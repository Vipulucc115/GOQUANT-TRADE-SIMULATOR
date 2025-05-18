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
      const url = `${config.apiUrl}simulate?quantity_usd=${quantity}&order_type=${orderType}&volume_30d=${volume30d}&exchange=${exchange}&asset=${asset}`;
      console.log('Fetching from URL:', url);
      
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        mode: 'cors',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ error: 'Unknown error occurred' }));
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Received data:', data);
      
      if (data.error) {
        throw new Error(data.error);
      }
      
      setResult(data);
    } catch (err) {
      console.error('Error:', err);
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const formatValue = (value: number, isPercentage: boolean = false) => {
    const formatted = isPercentage 
      ? (value * 100).toFixed(2) + '%'
      : value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 4 });
    
    return value >= 0 ? (
      <span className="positive-value">{formatted}</span>
    ) : (
      <span className="negative-value">{formatted}</span>
    );
  };

  return (
    <div className="trade-simulator-container">
      <div className="left-panel">
        <h2>Input Parameters</h2>
        <div className="input-group">
          <label>Quantity (USD):</label>
          <input 
            type="number" 
            value={quantity} 
            onChange={(e) => setQuantity(Number(e.target.value))}
            disabled={loading}
          />
        </div>
        <div className="input-group">
          <label>Order Type:</label>
          <select 
            value={orderType} 
            onChange={(e) => setOrderType(e.target.value as 'buy' | 'sell')}
            disabled={loading}
          >
            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
          </select>
        </div>
        <div className="input-group">
          <label>30-Day Volume (USD):</label>
          <input 
            type="number" 
            value={volume30d} 
            onChange={(e) => setVolume30d(Number(e.target.value))}
            disabled={loading}
          />
        </div>
        <div className="input-group">
          <label>Exchange:</label>
          <select 
            value={exchange} 
            onChange={(e) => setExchange(e.target.value)}
            disabled={loading}
          >
            <option value="OKX">OKX</option>
          </select>
        </div>
        <div className="input-group">
          <label>Asset:</label>
          <select 
            value={asset} 
            onChange={(e) => setAsset(e.target.value)}
            disabled={loading}
          >
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
        {loading && (
          <div className="loading-overlay">
            <div className="loading-spinner"></div>
          </div>
        )}
        {result ? (
          <div className="output">
            <p>
              <span>Order Type:</span>
              <span>{result.order_type.toUpperCase()}</span>
            </p>
            <p>
              <span>Filled Quantity:</span>
              <span>{formatValue(result.filled_quantity)}</span>
            </p>
            <p>
              <span>Average Price:</span>
              <span>{formatValue(result.avg_price)}</span>
            </p>
            <p>
              <span>Slippage:</span>
              <span>{formatValue(result.slippage, true)}</span>
            </p>
            <p>
              <span>Regression Slippage:</span>
              <span>{formatValue(result.reg_slippage, true)}</span>
            </p>
            <p>
              <span>Mid Price:</span>
              <span>{formatValue(result.mid_price)}</span>
            </p>
            <p>
              <span>Fees:</span>
              <span>{formatValue(result.fees.fee_amount)} ({result.fees.fee_tier})</span>
            </p>
            <p>
              <span>Market Impact:</span>
              <span>{formatValue(result.market_impact, true)}</span>
            </p>
            <p>
              <span>Net Cost:</span>
              <span>{formatValue(result.net_cost)}</span>
            </p>
            <p>
              <span>Volatility:</span>
              <span>{formatValue(result.volatility, true)}</span>
            </p>
            <p>
              <span>Processing Time:</span>
              <span>{result.processing_time_ms} ms</span>
            </p>
            <p>
              <span>Optimal Schedule:</span>
              <span>{formatValue(result.optimal_schedule)}</span>
            </p>
            <p>
              <span>Maker Probability:</span>
              <span>{formatValue(result.maker_prob, true)}</span>
            </p>
            <p>
              <span>Taker Probability:</span>
              <span>{formatValue(result.taker_prob, true)}</span>
            </p>
          </div>
        ) : (
          <div className="output-placeholder">
            {loading ? 'Simulating...' : 'No simulation results yet'}
          </div>
        )}
      </div>
    </div>
  );
};

export default TradeSimulator; 