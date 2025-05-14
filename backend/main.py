from fastapi import FastAPI, WebSocket, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging
from utils.websocket_client import connect_to_orderbook
from simulator import simulate_market_order
from typing import Literal
import os

app = FastAPI(
    title="GoQuant Trade Simulator",
    description="A high-performance trade simulator for estimating transaction costs and market impact",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],  # Allow both local and Vercel deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("uvicorn")

@app.on_event("startup")
async def startup_event():
    logger.info("Starting GoQuant Trade Simulator backend...")
    asyncio.create_task(connect_to_orderbook())  # background task

@app.get("/")
async def root():
    return {"message": "GoQuant Trade Simulator API is running"}

@app.get("/simulate")
async def run_simulation(
    quantity_usd: float = Query(100.0, description="Amount in USD to trade"),
    order_type: Literal["buy", "sell"] = Query("buy", description="Order type (buy/sell)"),
    volume_30d: float = Query(0.0, description="30-day trading volume for fee tier calculation"),
    exchange: str = Query("OKX", description="Exchange name (e.g., OKX)"),
    asset: str = Query("BTC-USDT-SWAP", description="Asset symbol (e.g., BTC-USDT-SWAP)")
):
    """
    Simulate a market order and calculate various metrics including:
    - Expected Slippage
    - Expected Fees
    - Expected Market Impact (Almgren-Chriss model)
    - Net Cost
    - Processing Time
    - Volatility
    - Optimal Execution Schedule
    """
    result = await simulate_market_order(quantity_usd, order_type, volume_30d, exchange, asset)
    return result
