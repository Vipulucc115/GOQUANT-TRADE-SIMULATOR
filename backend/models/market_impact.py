import numpy as np
from typing import Tuple

class AlmgrenChrissModel:
    def __init__(self, volatility: float, market_impact: float, risk_aversion: float = 0.1):
        """
        Initialize the Almgren-Chriss model for market impact calculation.
        
        Args:
            volatility (float): Market volatility (annualized)
            market_impact (float): Temporary market impact parameter
            risk_aversion (float): Risk aversion parameter (default: 0.1)
        """
        self.volatility = volatility
        self.market_impact = market_impact
        self.risk_aversion = risk_aversion

    def calculate_optimal_execution(self, 
                                  total_quantity: float, 
                                  time_horizon: float, 
                                  initial_price: float) -> Tuple[float, float]:
        """
        Calculate optimal execution strategy and expected market impact.
        
        Args:
            total_quantity (float): Total quantity to execute
            time_horizon (float): Time horizon in days
            initial_price (float): Initial market price
            
        Returns:
            Tuple[float, float]: (Expected market impact, Optimal execution schedule)
        """
        # Convert time horizon to years
        T = time_horizon / 365.0
        
        # Calculate optimal trading rate
        eta = np.sqrt(self.risk_aversion * self.volatility**2 / self.market_impact)
        
        # Calculate expected market impact
        market_impact = self.market_impact * total_quantity * initial_price
        
        # Calculate optimal execution schedule
        optimal_schedule = total_quantity * (1 - np.exp(-eta * T)) / (1 - np.exp(-eta * T))
        
        return market_impact, optimal_schedule

    def calculate_permanent_impact(self, quantity: float, initial_price: float) -> float:
        """
        Calculate permanent market impact.
        
        Args:
            quantity (float): Order quantity
            initial_price (float): Initial market price
            
        Returns:
            float: Permanent market impact
        """
        return self.market_impact * quantity * initial_price 