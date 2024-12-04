from typing import List
from Backend.GameManagement.playerGroupings.player import Player

DEFAULT_LIST = []

class TurnOrder():
    """Manages the order of turnsin the game."""
    def __init__(self, turn_order: List[Player] = DEFAULT_LIST):
        self._turn_order: List[Player] = turn_order

    def add_player(self, player: Player):
        pass

    def remove_player(self, player_id: int):
        pass

    def get_current_turn(self):
        pass

    def advance_turn(self):
        pass

    def reverse_turn_order(self):
        pass

    def get_turn_order(self) -> List[Player]:
        return self._turn_order
