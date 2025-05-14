import React, { useState } from 'react';
import './TradeSimulator.css';
import config from '../config';

interface SimulationResult {
  order_type: string;
  filled_quantity: number;
  avg_price: number;
  slippage: number;
  mid_price: number;
  fees: {
    fee_rate: number;
    fee_amount: number;
    fee_tier: string;
    order_value: number;
  };
  market_impact: number;
  net_cost: number;
  volatility: number;
  processing_time_ms: number;
  optimal_schedule: number;
  reg_slippage: number;
  maker_prob: number;
  taker_prob: number;
}

const TradeSimulator: React.FC = () => {
  const [quantity, setQuantity] = useState<number>(100);
  const [orderType, setOrderType] = useState<'buy' | 'sell'>('buy');
  const [volume30d, setVolume30d] = useState<number>(0);
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [exchange, setExchange] = useState<string>("OKX");
  const [asset, setAsset] = useState<string>("BTC-USDT-SWAP");

  const handleSimulate = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`${config.apiUrl}/simulate?quantity_usd=${quantity}&order_type=${orderType}&volume_30d=${volume30d}&exchange=${exchange}&asset=${asset}`);
      if (!response.ok) {
        throw new Error('Simulation failed');
      }
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="trade-simulator-container">
      <div className="left-panel">
        <h2>Input Parameters</h2>
        <div className="input-group">
          <label>Quantity (USD):</label>
          <input type="number" value={quantity} onChange={(e) => setQuantity(Number(e.target.value))} />
        </div>
        <div className="input-group">
          <label>Order Type:</label>
          <select value={orderType} onChange={(e) => setOrderType(e.target.value as 'buy' | 'sell')}>
            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
          </select>
        </div>
        <div className="input-group">
          <label>30-Day Volume (USD):</label>
          <input type="number" value={volume30d} onChange={(e) => setVolume30d(Number(e.target.value))} />
        </div>
        <div className="input-group">
          <label>Exchange:</label>
          <select value={exchange} onChange={(e) => setExchange(e.target.value)}>
            <option value="OKX">OKX</option>
          </select>
        </div>
        <div className="input-group">
          <label>Asset:</label>
          <select value={asset} onChange={(e) => setAsset(e.target.value)}>
            <option value="BTC-USDT-SWAP">BTC-USDT-SWAP</option>
            <option value="ETH-USDT-SPOT">ETH-USDT-SPOT</option>
          </select>
        </div>
        <button onClick={handleSimulate} disabled={loading}>
          {loading ? 'Simulating...' : 'Simulate'}
        </button>
        {error && <div className="error">{error}</div>}
      </div>
      <div className="right-panel">
        <h2>Simulation Output</h2>
        {result ? (
          <div className="output">
            <p>Order Type: {result.order_type}</p>
            <p>Filled Quantity: {result.filled_quantity}</p>
            <p>Average Price: {result.avg_price}</p>
            <p>Slippage: {result.slippage}</p>
            <p>Regression Slippage: {result.reg_slippage}</p>
            <p>Mid Price: {result.mid_price}</p>
            <p>Fees: {result.fees.fee_amount} ({result.fees.fee_tier})</p>
            <p>Market Impact: {result.market_impact}</p>
            <p>Net Cost: {result.net_cost}</p>
            <p>Volatility: {result.volatility}</p>
            <p>Processing Time: {result.processing_time_ms} ms</p>
            <p>Optimal Schedule: {result.optimal_schedule}</p>
            <p>Maker Probability: {(result.maker_prob * 100).toFixed(2)}%</p>
            <p>Taker Probability: {(result.taker_prob * 100).toFixed(2)}%</p>
          </div>
        ) : (
          <div className="output-placeholder">No simulation results yet</div>
        )}
      </div>
    </div>
  );
};

export default TradeSimulator; 