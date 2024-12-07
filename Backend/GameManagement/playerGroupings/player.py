
from __future__ import annotations
from Backend.cardGroupings.Card import Card
from Backend.cardGroupings.Hand import Hand
from Backend.cardGroupings.Card import Card
from Backend.gameboardGroupings.space import Space, SpaceType
from Backend.GameManagement.playerGroupings.player_turn import Player_Turn
class Player():


    def __init__(self, name: str):
        self.playerName = name
        self.isEliminated = False
        self._player_turn = Player_Turn()
        self.playerID: int = -1
        self.character: str = None
        self.playerHand: Hand = Hand()
        self.currLocation: 'Space' = None
        self.prevLocation: 'Space' = None

    def receive_card_dealt(self, card: Card):
        self.playerHand.add_card(card)

    def get_valid_moves(self) -> list['Space']:
        # returns a list of Space objects
        adj: list['Space'] = self.currLocation.get_adjacent_spaces()

        possible_dest = []
        # check if adjacent spaces are empty
        for sp in adj:
            if 'SpaceType'.HALLWAY == sp.get_space_type():
                if sp.is_empty():
                    possible_dest.append(sp)
            else:
                possible_dest.append(sp)
        return possible_dest

    def get_player_turn(self) -> Player_Turn:
        return self._player_turn

    def get_player_name(self) -> str:
        return self.playerName

    def get_hand(self) -> Hand:
        return self.playerHand

    def get_character(self) -> str:
        return self.character

    def get_current_location(self) -> 'Space':
        return self.currLocation

    def get_previous_location(self) -> 'Space':
        return self.prevLocation

    def set_current_location(self, sp: 'Space') -> bool:
        if SpaceType.HALLWAY ==  sp.get_space_type() and not sp.is_empty():
                return False
        if None != self.currLocation:
            self.currLocation.remove_player_count()

        self.prevLocation = self.currLocation
        self.currLocation = sp
        self.currLocation.add_player_count()
        return True

    def is_eliminated(self) -> bool:
        return self.isEliminated

    def __str__(self):
        return self.character



