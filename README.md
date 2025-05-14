# GoQuant Trade Simulator

A high-performance trade simulator leveraging real-time market data to estimate transaction costs and market impact. Built for the GoQuant assignment.

## Features
- Real-time L2 orderbook data from OKX (WebSocket)
- User interface with input (left) and output (right) panels
- Supports exchange and asset selection (OKX, BTC-USDT-SWAP, ETH-USDT-SPOT)
- Simulates market orders with:
  - Slippage (direct and regression-based)
  - Fees (rule-based, fee tier)
  - Market impact (Almgren-Chriss model)
  - Net cost
  - Maker/taker proportion (logistic regression)
  - Volatility
  - Processing time (latency)
- Error handling and logging
- Modular, maintainable codebase
- Backend and frontend test cases

## Models & Algorithms
- **Slippage Regression:** Linear regression on order size and volatility
- **Maker/Taker Proportion:** Logistic regression on order size and volatility
- **Market Impact:** Almgren-Chriss optimal execution model
- **Fee Model:** Rule-based, based on OKX fee tiers and 30d volume
- **Volatility:** Rolling window, annualized

See `MODELS.md` for detailed explanations and formulas.

## Performance
- Backend processes data faster than stream (see `PERFORMANCE.md`)
- Latency metrics: data processing, UI update, end-to-end
- Optimizations: async I/O, efficient data structures, minimal locking

## Testing
- Backend: `pytest backend/test_simulator.py`
- Frontend: `npm test` in `frontend/`

## Submission Checklist
- [x] Complete source code with documentation
- [x] Video demo (see below)
- [x] Performance analysis and optimization notes
- [x] Test cases for backend and frontend

## Video Demo
1. Show the UI in action (input, simulate, output updates)
2. Walk through the codebase (backend, frontend, models)
3. Explain models and performance

## How to Run
1. Start backend: `cd backend && uvicorn main:app --reload`
2. Start frontend: `cd frontend && npm start`
3. Open http://localhost:3000

---

For more details, see `MODELS.md` and `PERFORMANCE.md`.

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
