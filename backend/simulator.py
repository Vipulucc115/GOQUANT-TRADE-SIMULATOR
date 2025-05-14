from typing import Literal, Dict
from orderbook import orderbook
from models.market_impact import AlmgrenChrissModel
from models.fee_calculator import FeeCalculator
from models.volatility import VolatilityCalculator
import asyncio
import time
import numpy as np

# Initialize models
fee_calculator = FeeCalculator()
volatility_calculator = VolatilityCalculator()
market_impact_model = None  # Will be initialized with volatility

def logistic(x):
    return 1 / (1 + np.exp(-x))

def maker_taker_proportion(order_size, volatility):
    # Simple logistic regression: weights are arbitrary for demo
    w0, w1, w2 = -2, 0.01, -10
    x = w0 + w1 * order_size + w2 * volatility
    taker_prob = logistic(x)
    maker_prob = 1 - taker_prob
    return maker_prob, taker_prob

def slippage_regression(order_size, volatility):
    # Simple linear regression: coefficients are arbitrary for demo
    coef_size = 0.0001
    coef_vol = 0.5
    intercept = 0.01
    return intercept + coef_size * order_size + coef_vol * volatility

async def simulate_market_order(
    quantity_usd: float,
    order_type: Literal["buy", "sell"],
    volume_30d: float = 0,
    exchange: str = "OKX",
    asset: str = "BTC-USDT-SWAP"
) -> Dict:
    """
    Simulate a market order and calculate all metrics.
    
    Args:
        quantity_usd (float): Order quantity in USD
        order_type (str): 'buy' or 'sell'
        volume_30d (float): 30-day trading volume for fee tier calculation
        exchange (str): Exchange name
        asset (str): Asset name
        
    Returns:
        Dict: Simulation results including all metrics
    """
    # Log the selected exchange and asset
    print(f"Simulating for exchange: {exchange}, asset: {asset}")
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

    avg_execution_price = cost / filled_qty
    filled_value = filled_qty * avg_execution_price
    if filled_qty == 0 or filled_value < 0.99 * quantity_usd:
        return {"error": "Insufficient liquidity"}

    # Calculate metrics
    slippage = avg_execution_price - mid_price if order_type == "buy" else mid_price - avg_execution_price
    # Regression-based slippage estimate
    reg_slippage = slippage_regression(filled_qty, current_volatility)
    # Maker/taker proportion
    maker_prob, taker_prob = maker_taker_proportion(filled_qty, current_volatility)
    
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
        "reg_slippage": reg_slippage,
        "mid_price": mid_price,
        "fees": fee_details,
        "market_impact": market_impact,
        "net_cost": net_cost,
        "volatility": current_volatility,
        "processing_time_ms": processing_time * 1000,
        "optimal_schedule": optimal_schedule,
        "maker_prob": maker_prob,
        "taker_prob": taker_prob
    }
