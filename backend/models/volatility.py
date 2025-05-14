import numpy as np
from typing import List, Tuple
from collections import deque

class VolatilityCalculator:
    def __init__(self, window_size: int = 100):
        """
        Initialize volatility calculator with a rolling window.
        
        Args:
            window_size (int): Size of the rolling window for volatility calculation
        """
        self.window_size = window_size
        self.price_history = deque(maxlen=window_size)
        self.returns = deque(maxlen=window_size-1)

    def update(self, price: float) -> float:
        """
        Update volatility calculation with new price.
        
        Args:
            price (float): New price to add to the calculation
            
        Returns:
            float: Current volatility estimate
        """
        self.price_history.append(price)
        
        if len(self.price_history) > 1:
            # Calculate return
            prev_price = self.price_history[-2]
            current_return = np.log(price / prev_price)
            self.returns.append(current_return)
            
            # Calculate volatility (annualized)
            if len(self.returns) > 1:
                volatility = np.std(self.returns) * np.sqrt(252)  # Annualized
                return volatility
        
        return 0.0

    def get_volatility(self) -> float:
        """
        Get current volatility estimate.
        
        Returns:
            float: Current volatility estimate (annualized)
        """
        if len(self.returns) > 1:
            return np.std(self.returns) * np.sqrt(252)
        return 0.0

    def get_historical_volatility(self, prices: List[float], window: int = 20) -> List[float]:
        """
        Calculate historical volatility for a series of prices.
        
        Args:
            prices (List[float]): List of historical prices
            window (int): Window size for volatility calculation
            
        Returns:
            List[float]: List of historical volatility values
        """
        if len(prices) < 2:
            return [0.0]
            
        # Calculate returns
        returns = np.log(np.array(prices[1:]) / np.array(prices[:-1]))
        
        # Calculate rolling volatility
        volatilities = []
        for i in range(len(returns) - window + 1):
            window_returns = returns[i:i+window]
            vol = np.std(window_returns) * np.sqrt(252)
            volatilities.append(vol)
            
        return volatilities 