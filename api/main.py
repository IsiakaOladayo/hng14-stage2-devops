from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import redis
import uuid
import os
import logging

logging.basicConfig(level=logging.INFO)

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
QUEUE_NAME = os.getenv("QUEUE_NAME", "job")

r = redis.Redis(host=REDIS_HOST, port=6379)

@app.post("/jobs")
def create_job():
    try:
        job_id = str(uuid.uuid4())
        r.lpush(QUEUE_NAME, job_id)
        r.hset(f"job:{job_id}", "status", "queued")
        return {"job_id": job_id}
    except redis.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Redis unavailable")

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return JSONResponse(content={"id": job_id})

@app.get("/health")
def health():
    return {"status": "ok"}
