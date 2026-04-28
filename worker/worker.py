import redis
import time
import os
import signal
import logging

logging.basicConfig(level=logging.INFO)

# ✅ FIX 1: correct Docker hostname
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
QUEUE_NAME = os.getenv("QUEUE_NAME", "job")

# ✅ FIX 2: decode responses automatically
r = redis.Redis(
    host=REDIS_HOST,
    port=6379,
    decode_responses=True
)

running = True

def shutdown(sig, frame):
    global running
    logging.info("Shutting down worker...")
    running = False

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

def process_job(job_id):
    logging.info(f"Processing job {job_id}")

    # simulate work
    time.sleep(2)

    r.hset(f"job:{job_id}", mapping={
        "status": "completed"
    })

    logging.info(f"Done: {job_id}")

while running:
    try:
        job = r.brpop(QUEUE_NAME, timeout=5)

        if not job:
            continue

        _, job_id = job

        process_job(job_id)

    except redis.exceptions.ConnectionError:
        logging.error("Redis not ready, retrying...")
        time.sleep(2)