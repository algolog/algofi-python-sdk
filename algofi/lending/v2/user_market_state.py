# IMPORTS
from base64 import b64decode

from .lending_config import MANAGER_STRINGS, MARKET_STRINGS

# INTERFACE
from ...utils import int_to_bytes, bytes_to_int


class UserMarketState:
    def __init__(self, market, state):
        self.b_asset_collateral = state.get(MARKET_STRINGS.user_active_b_asset_collateral, 0)
        self.borrow_shares = state.get(MARKET_STRINGS.user_borrow_shares, 0)
        self.supplied_amount = market.b_asset_to_asset_amount(self.b_asset_collateral)
        self.borrowed_amount = market.borrow_shares_to_asset_amount(self.borrow_shares)
        self.rewards_states = []
        for i in range(market.max_rewards_program_index + 1):
            self.rewards_states.append(UserRewardsState(state, i))

class UserRewardsState:
    def __init__(self, state, program_index):
        program_index_bytestr = int_to_bytes(program_index).decode()
        program_index_key = MARKET_STRINGS.user_rewards_program_number_prefix + program_index_bytestr
        latest_rewards_index_key = MARKET_STRINGS.user_latest_rewards_index_prefix + program_index_bytestr
        unclaimed_rewards_key = MARKET_STRINGS.user_unclaimed_rewards_prefix + program_index_bytestr

        self.rewards_program_number = state.get(program_index_key, 0)
        self.latest_rewards_index = bytes_to_int(b64decode(state.get(latest_rewards_index_key, 0)))
        self.unclaimed_rewards = state.get(unclaimed_rewards_key, 0)
