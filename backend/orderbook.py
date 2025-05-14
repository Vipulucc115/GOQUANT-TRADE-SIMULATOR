import asyncio
from collections import deque
from typing import List, Tuple

# OrderBookSnapshot holds current top N levels of bids and asks
class OrderBook:
    def __init__(self, depth: int = 20):
        self.bids: List[Tuple[float, float]] = []
        self.asks: List[Tuple[float, float]] = []
        self.depth = depth
        self.lock = asyncio.Lock()

    async def update(self, bids: List[List[str]], asks: List[List[str]]):
        async with self.lock:
            self.bids = sorted(
                [(float(price), float(size)) for price, size in bids[:self.depth]],
                key=lambda x: -x[0]
            )
            self.asks = sorted(
                [(float(price), float(size)) for price, size in asks[:self.depth]],
                key=lambda x: x[0]
            )
            # logger.info(f"Updated bids: {self.bids[:5]}")  # Debugging line
            # logger.info(f"Updated asks: {self.asks[:5]}")  # Debugging line

    async def get_snapshot(self):
        async with self.lock:
            return self.bids.copy(), self.asks.copy()

# Create a singleton instance
orderbook = OrderBook(depth=20)
