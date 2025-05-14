from typing import Literal, Dict
from orderbook import orderbook
from models.market_impact import AlmgrenChrissModel
from models.fee_calculator import FeeCalculator
from models.volatility import VolatilityCalculator
import asyncio
import time

# Initialize models
fee_calculator = FeeCalculator()
volatility_calculator = VolatilityCalculator()
market_impact_model = None  # Will be initialized with volatility

async def simulate_market_order(
    quantity_usd: float,
    order_type: Literal["buy", "sell"],
    volume_30d: float = 0
) -> Dict:
    """
    Simulate a market order and calculate all metrics.
    
    Args:
        quantity_usd (float): Order quantity in USD
        order_type (str): 'buy' or 'sell'
        volume_30d (float): 30-day trading volume for fee tier calculation
        
    Returns:
        Dict: Simulation results including all metrics
    """
    start_time = time.time()
    
    # Get orderbook snapshot
    bids, asks = await orderbook.get_snapshot()

    if not bids or not asks:
        return {"error": "Order book is empty"}

    # Calculate mid price
    mid_price = (bids[0][0] + asks[0][0]) / 2
    
    # Update volatility calculator
    current_volatility = volatility_calculator.update(mid_price)
    
    # Initialize market impact model with current volatility
    market_impact_model = AlmgrenChrissModel(
        volatility=current_volatility,
        market_impact=0.1  # This should be calibrated based on historical data
    )

    # Calculate execution metrics
    qty_remaining = quantity_usd
    filled_qty = 0
    cost = 0
    execution_prices = []

    if order_type == "buy":
        book = asks
    else:
        book = bids

    for price, size in book:
        level_value = price * size
        execution_prices.append(price)

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

    # Calculate metrics
    avg_execution_price = cost / filled_qty
    slippage = avg_execution_price - mid_price if order_type == "buy" else mid_price - avg_execution_price
    
    # Calculate fees
    fee_details = fee_calculator.calculate_fee(
        order_type="taker",  # Market orders are always taker
        volume=filled_qty,
        price=avg_execution_price,
        volume_30d=volume_30d
    )
    
    # Calculate market impact
    market_impact, optimal_schedule = market_impact_model.calculate_optimal_execution(
        total_quantity=filled_qty,
        time_horizon=1.0,  # 1 day horizon
        initial_price=mid_price
    )
    
    # Calculate net cost
    net_cost = slippage + fee_details["fee_amount"] + market_impact
    
    # Calculate processing time
    processing_time = time.time() - start_time
    
    return {
        "order_type": order_type,
        "filled_quantity": filled_qty,
        "avg_price": avg_execution_price,
        "slippage": slippage,
        "mid_price": mid_price,
        "fees": fee_details,
        "market_impact": market_impact,
        "net_cost": net_cost,
        "volatility": current_volatility,
        "processing_time_ms": processing_time * 1000,
        "optimal_schedule": optimal_schedule
    }
