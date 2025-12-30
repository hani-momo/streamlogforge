from fastapi import FastAPI, HTTPException
from aiokafka import AIOKafkaProducer
import asyncio
from schemas import LogEvent
import json

app = FastAPI(title="Ingestion API")

KAFKA_BOOTSTRAP = "redpanda:9092"
TOPIC = "raw_logs"

producer: AIOKafkaProducer = None

@app.on_event("startup")
async def startup_event():
    global producer
    producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP)
    await producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()

@app.post("/logs")
async def ingest_log(event: LogEvent):
    try:
        await producer.send_and_wait(TOPIC, event.json().encode("utf-8"))
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
