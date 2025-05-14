# Models & Algorithms

## Slippage Regression
A simple linear regression is used to estimate slippage as a function of order size and volatility:

    slippage = intercept + coef_size * order_size + coef_vol * volatility

Where coefficients are chosen for demonstration. In production, these would be fit to historical data.

## Maker/Taker Proportion (Logistic Regression)
A logistic regression estimates the probability of an order being a maker or taker:

    taker_prob = 1 / (1 + exp(-(w0 + w1 * order_size + w2 * volatility)))
    maker_prob = 1 - taker_prob

Weights are chosen for demonstration. In production, these would be fit to labeled data.

## Market Impact (Almgren-Chriss Model)
The Almgren-Chriss model is used to estimate optimal execution and market impact:

    market_impact = market_impact_param * total_quantity * initial_price
    optimal_schedule = ... (see code for details)

## Fee Model
Fees are calculated using a rule-based model based on OKX's published fee tiers and the user's 30-day trading volume. Taker fees are used for market orders.

## Volatility
Volatility is calculated using a rolling window of log returns, annualized:

    volatility = std(log_returns) * sqrt(252)

---

For more details, see the code in `backend/models/` and `backend/simulator.py`. 