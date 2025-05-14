from fastapi import FastAPI, WebSocket, Query
import asyncio
import logging
from utils.websocket_client import connect_to_orderbook
from simulator import simulate_market_order


app = FastAPI()
logger = logging.getLogger("uvicorn")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting GoQuant Trade Simulator backend...")
    asyncio.create_task(connect_to_orderbook())  # background task

@app.get("/")
def root():
    return {"message": "GoQuant Trade Simulator Backend Running"}

@app.get("/simulate")
async def run_simulation(
    quantity_usd: float = Query(100.0, description="Amount in USD to trade"),
    order_type: str = Query("buy", enum=["buy", "sell"])
):
    result = await simulate_market_order(quantity_usd, order_type)
    return result
