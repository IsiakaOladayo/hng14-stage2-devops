from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import redis
import uuid
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

# ✅ FIX 1: correct default for Docker
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
QUEUE_NAME = os.getenv("QUEUE_NAME", "job")

r = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)

# -------------------------
# CREATE JOB
# -------------------------
@app.post("/submit")
def create_job():
    try:
        job_id = str(uuid.uuid4())

        r.lpush(QUEUE_NAME, job_id)

        r.hset(f"job:{job_id}", mapping={
            "status": "queued"
        })

        return {"id": job_id, "status": "queued"}

    except redis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Redis unavailable")


# -------------------------
# GET JOB
# -------------------------
@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")

    if status is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {"id": job_id, "status": status}


# -------------------------
# HEALTH CHECK
# -------------------------
@app.get("/health")
def health():
    return {"status": "ok"}