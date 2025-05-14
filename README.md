# GoQuant Trade Simulator

A high-performance trade simulator that leverages real-time market data to estimate transaction costs and market impact for cryptocurrency trading.

## Features

- Real-time L2 orderbook data processing
- Market order simulation with slippage calculation
- Fee calculation based on OKX's fee structure
- Market impact estimation using Almgren-Chriss model
- Volatility calculation
- Performance metrics and latency tracking

## Prerequisites

- Python 3.8+
- Node.js 16+ (for frontend)
- VPN connection (required for OKX data access)

## Backend Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the backend server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET /simulate
Simulates a market order and returns various metrics.

Parameters:
- `quantity_usd` (float): Amount in USD to trade (default: 100.0)
- `order_type` (str): Order type - "buy" or "sell" (default: "buy")
- `volume_30d` (float): 30-day trading volume for fee tier calculation (default: 0.0)

Response includes:
- Expected Slippage
- Expected Fees
- Expected Market Impact
- Net Cost
- Processing Time
- Volatility
- Optimal Execution Schedule

## Models

### Almgren-Chriss Model
Implementation of the Almgren-Chriss model for market impact calculation, considering:
- Volatility
- Market impact
- Risk aversion
- Time horizon

### Fee Calculator
Implements OKX's fee structure with:
- Multiple fee tiers
- Maker/Taker fee differentiation
- Volume-based discounts

### Volatility Calculator
Calculates market volatility using:
- Rolling window approach
- Log returns
- Annualized volatility

## Performance Considerations

- Real-time data processing
- Efficient orderbook management
- Optimized market impact calculations
- Latency tracking and monitoring

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is proprietary and confidential.
