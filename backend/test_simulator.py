import pytest
import asyncio
from simulator import simulate_market_order

class DummyOrderBook:
    async def get_snapshot(self):
        # Return a simple orderbook for testing
        bids = [(10000, 1), (9990, 2)]
        asks = [(10010, 1.5), (10020, 2)]
        return bids, asks

@pytest.mark.asyncio
async def test_basic_simulation(monkeypatch):
    # Patch the orderbook in simulator
    from simulator import orderbook as real_orderbook
    monkeypatch.setattr(real_orderbook, 'get_snapshot', DummyOrderBook().get_snapshot)
    result = await simulate_market_order(100, 'buy', 50000, 'OKX', 'BTC-USDT-SWAP')
    assert 'filled_quantity' in result
    assert 'slippage' in result
    assert 'reg_slippage' in result
    assert 'maker_prob' in result
    assert 'taker_prob' in result
    assert result['fees']['fee_tier'] == 'tier2'

@pytest.mark.asyncio
async def test_maker_taker_proportion(monkeypatch):
    from simulator import orderbook as real_orderbook
    monkeypatch.setattr(real_orderbook, 'get_snapshot', DummyOrderBook().get_snapshot)
    result = await simulate_market_order(100, 'buy', 0, 'OKX', 'BTC-USDT-SWAP')
    assert 0 <= result['maker_prob'] <= 1
    assert 0 <= result['taker_prob'] <= 1
    assert abs(result['maker_prob'] + result['taker_prob'] - 1) < 1e-6

@pytest.mark.asyncio
async def test_regression_slippage(monkeypatch):
    from simulator import orderbook as real_orderbook
    monkeypatch.setattr(real_orderbook, 'get_snapshot', DummyOrderBook().get_snapshot)
    result = await simulate_market_order(100, 'buy', 0, 'OKX', 'BTC-USDT-SWAP')
    assert isinstance(result['reg_slippage'], float)

@pytest.mark.asyncio
async def test_empty_orderbook(monkeypatch):
    class EmptyOrderBook:
        async def get_snapshot(self):
            return [], []
    from simulator import orderbook as real_orderbook
    monkeypatch.setattr(real_orderbook, 'get_snapshot', EmptyOrderBook().get_snapshot)
    result = await simulate_market_order(100, 'buy', 0, 'OKX', 'BTC-USDT-SWAP')
    assert 'error' in result
    assert result['error'] == 'Order book is empty'

@pytest.mark.asyncio
async def test_insufficient_liquidity(monkeypatch):
    class SmallOrderBook:
        async def get_snapshot(self):
            return [(10000, 0.001)], [(10010, 0.001)]
    from simulator import orderbook as real_orderbook
    monkeypatch.setattr(real_orderbook, 'get_snapshot', SmallOrderBook().get_snapshot)
    result = await simulate_market_order(1000000, 'buy', 0, 'OKX', 'BTC-USDT-SWAP')
    assert 'error' in result
    assert result['error'] == 'Insufficient liquidity' 