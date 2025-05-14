const config = {
    apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    wsUrl: process.env.NEXT_PUBLIC_WS_URL || 'wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP'
};

export default config; 