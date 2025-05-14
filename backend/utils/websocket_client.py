import websockets
import asyncio
import json
import logging
from orderbook import orderbook

logger = logging.getLogger("uvicorn")

WS_URL = "wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP"

async def connect_to_orderbook():
    while True:
        try:
            async with websockets.connect(WS_URL) as websocket:
                logger.info("✅ Connected to OKX L2 Order Book WebSocket")

                async for message in websocket:
                    data = json.loads(message)
                    bids = data.get("bids", [])
                    asks = data.get("asks", [])

                    if bids and asks:
                        logger.info(f"Received data: Bids: {bids[:5]} | Asks: {asks[:5]}")
                    else:
                        logger.warning("Received empty bids/asks data!")

                    await orderbook.update(bids, asks)

                    top_bid = bids[0] if bids else ["-", "-"]
                    top_ask = asks[0] if asks else ["-", "-"]
                    logger.info(f"Bid: {top_bid} | Ask: {top_ask}")

        except Exception as e:
            logger.error(f"WebSocket error: {e}")
            logger.info("🔁 Reconnecting in 3 seconds...")
            await asyncio.sleep(3)
