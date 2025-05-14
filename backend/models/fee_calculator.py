from typing import Literal, Dict

class FeeCalculator:
    def __init__(self):
        # OKX fee tiers (as of 2024)
        self.fee_tiers = {
            "tier1": {"maker": 0.0008, "taker": 0.001},  # < 50,000 USDT
            "tier2": {"maker": 0.0007, "taker": 0.0009},  # 50,000 - 100,000 USDT
            "tier3": {"maker": 0.0006, "taker": 0.0008},  # 100,000 - 500,000 USDT
            "tier4": {"maker": 0.0005, "taker": 0.0007},  # 500,000 - 1,000,000 USDT
            "tier5": {"maker": 0.0004, "taker": 0.0006},  # > 1,000,000 USDT
        }

    def get_fee_tier(self, volume_30d: float) -> str:
        """
        Determine fee tier based on 30-day trading volume.
        
        Args:
            volume_30d (float): 30-day trading volume in USDT
            
        Returns:
            str: Fee tier name
        """
        if volume_30d >= 1000000:
            return "tier5"
        elif volume_30d >= 500000:
            return "tier4"
        elif volume_30d >= 100000:
            return "tier3"
        elif volume_30d >= 50000:
            return "tier2"
        else:
            return "tier1"

    def calculate_fee(self, 
                     order_type: Literal["maker", "taker"],
                     volume: float,
                     price: float,
                     volume_30d: float = 0) -> Dict[str, float]:
        """
        Calculate trading fees for an order.
        
        Args:
            order_type (str): 'maker' or 'taker'
            volume (float): Order volume in base currency
            price (float): Order price in quote currency
            volume_30d (float): 30-day trading volume in USDT
            
        Returns:
            Dict[str, float]: Fee details including rate and amount
        """
        # Get fee tier
        tier = self.get_fee_tier(volume_30d)
        fee_rate = self.fee_tiers[tier][order_type]
        
        # Calculate fee amount
        order_value = volume * price
        fee_amount = order_value * fee_rate
        
        return {
            "fee_rate": fee_rate,
            "fee_amount": fee_amount,
            "fee_tier": tier,
            "order_value": order_value
        } 