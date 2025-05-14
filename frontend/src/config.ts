const config = {
    apiUrl: process.env.NEXT_PUBLIC_API_URL || 'https://goquant-trade-simulator-1.onrender.com/',
    wsUrl: process.env.NEXT_PUBLIC_WS_URL || 'wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP'
};

export default config; 