from fastapi import FastAPI
from aiokafka import AIOKafkaProducer
from sqlmodel import Field, Session, SQLModel, create_engine, select
import json
import asyncio

class order(SQLModel):
    order_id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(default=None,index=True)
    product_name: str
    

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/order")
async def create_order(order:order):
    producer = AIOKafkaProducer(bootstrap_servers='broker:19092')
    order_json = json.dumps(order.__dict__).encode("utf-8")
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait("order", order_json)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()
    return order_json