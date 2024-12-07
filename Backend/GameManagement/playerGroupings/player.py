
from __future__ import annotations
from Backend.cardGroupings.Card import Card
from Backend.cardGroupings.Hand import Hand
from Backend.gameboardGroupings.space import Space, SpaceType
from Backend.GameManagement.playerGroupings.player_turn import Player_Turn


class Player():

    def __init__(self, player_name: str, player_id: int):
        self.playerName = player_name
        self.isEliminated = False
        self._player_turn = Player_Turn()
        self.playerID: int = player_id
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

    def get_player_id(self) -> int:
        return self.playerID

    def get_current_location(self) -> 'Space' | None:
        return self.currLocation

    def get_previous_location(self) -> 'Space' | None:
        return self.prevLocation

    def set_current_location(self, sp: 'Space') -> bool:
        if SpaceType.HALLWAY == sp.get_space_type() and not sp.is_empty():
            return False
        if self.currLocation is not None:
            self.currLocation.remove_player_count()

        self.prevLocation = self.currLocation
        self.currLocation = sp
        self.currLocation.add_player_count()
        return True

    def set_player_name(self, player_name: str):
        # TODO: Add a check to ensure that player
        self.playerName = player_name

    def set_player_id(self, player_id: str):
        # TODO: Add a check to ensure player_id is valid
        self.playerID = player_id

    def set_player_hand(self, hand: Hand):
        self.playerHand = hand

    def set_character(self, character_name: str):
        # TODO: Add a check to ensure a valid character name is set
        self.character = character_name

    def is_eliminated(self) -> bool:
        return self.isEliminated

    def __str__(self):
        return self.character
