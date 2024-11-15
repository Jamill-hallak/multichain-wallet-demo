class StakingSimulator:
    """
    Simulates staking rewards based on an annual percentage yield (APY).
    """

    def __init__(self, annual_yield=0.1):
        self.annual_yield = annual_yield  # Default 10% annual yield

    def simulate_rewards(self, staked_amount, months=12):
        """
        Calculate staking rewards for the specified duration.
        Args:
            staked_amount (float): The amount staked.
            months (int): The duration in months.
        Returns:
            float: The calculated staking rewards.
        """
        monthly_yield = self.annual_yield / 12
        return staked_amount * monthly_yield * months
