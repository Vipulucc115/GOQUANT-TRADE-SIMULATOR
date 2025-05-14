from typing import Literal
from orderbook import orderbook
import asyncio

async def simulate_market_order(quantity_usd: float, order_type: Literal["buy", "sell"]):
    bids, asks = await orderbook.get_snapshot()

    if not bids or not asks:
        return {"error": "Order book is empty"}

    mid_price = (bids[0][0] + asks[0][0]) / 2

    qty_remaining = quantity_usd
    filled_qty = 0
    cost = 0

    if order_type == "buy":
        book = asks
    else:
        book = bids

    for price, size in book:
        level_value = price * size

        if level_value >= qty_remaining:
            filled = qty_remaining / price
            cost += filled * price
            filled_qty += filled
            break
        else:
            cost += size * price
            filled_qty += size
            qty_remaining -= level_value

    if filled_qty == 0:
        return {"error": "Insufficient liquidity"}

    avg_execution_price = cost / filled_qty
    slippage = avg_execution_price - mid_price if order_type == "buy" else mid_price - avg_execution_price

    return {
        "order_type": order_type,
        "filled_quantity": filled_qty,
        "avg_price": avg_execution_price,
        "slippage": slippage,
        "mid_price": mid_price
    }
