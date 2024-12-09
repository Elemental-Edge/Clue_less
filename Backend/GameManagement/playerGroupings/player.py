from __future__ import annotations
from Backend.cardGroupings.Card import Card
from Backend.cardGroupings.Hand import Hand
from Backend.gameboardGroupings.space import Space, SpaceType
from Backend.GameManagement.playerGroupings.player_turn import Player_Turn


class Player:

    def __init__(self, char_name: str, playerID: int):
        self._playerID: int = playerID
        self._playerName = "TODO"
        self._character: str = char_name
        self._eliminated = False
        self._active = False
        self._player_turn = Player_Turn()
        self._playerHand: Hand = Hand()
        self._currLocation: Space = None
        self._prevLocation: Space = None

    def __eq__(self, other: object) -> bool:
        """Overloads the equality operator to check for space equality via
        memory address comparison"""
        if self is other:
            return True
        if self._playerID != other._playerID:
            return False
        if self._character != other._character:
            return False
        if self._eliminated != other._isEliminated:
            return False
        if self._currLocation != other._currLocation:
            return False
        if self._prevLocation != other._prevLocation:
            return False
        if self._active != other._active:
            return False
        return True

    def receive_card_dealt(self, card: Card):
        if self._active:
            self._playerHand.add_card(card)

    def get_valid_moves(self) -> list[Space]:
        # returns a list of Space objects
        possible_dest = []
        if self._active:
            adj: list[Space] = self._currLocation.get_adjacent_spaces()

            # check if adjacent spaces are empty
            for sp in adj:
                if SpaceType.HALLWAY == sp.get_space_type():
                    if sp.is_empty():
                        possible_dest.append(sp)
                else:
                    possible_dest.append(sp)
        return possible_dest
    
    def get_player_turn(self) -> Player_Turn:
        if self._active:
            return self._player_turn

    def get_player_name(self) -> str:
        return self._playerName

    def get_playerID(self):
        return self._playerID

    def get_hand(self) -> Hand:
        if self._active:
            return self._playerHand

    def get_character(self) -> str:
        return self._character

    def get_current_location(self) -> Space:
        return self._currLocation

    def get_previous_location(self) -> Space:
        return self._prevLocation
    
    def get_active(self) -> bool:
        return self._active
    
    def set_active(self, val: bool = True):
        self._active = bool

    def set_character(self, aCharacter: str):
        self._character = aCharacter

    def set_current_location(self, sp: Space) -> bool:
        if SpaceType.HALLWAY == sp.get_space_type() and not sp.is_empty():
            return False
        if None is not self._currLocation:
            self._currLocation.remove_player_count()

        self._prevLocation = self._currLocation
        self._currLocation = sp
        self._currLocation.add_player_count()
        return True

    def set_player_name(self, player_name: str):
        # TODO: Add a check to ensure that player
        self.playerName = player_name

    def set_player_id(self, player_id: str):
        # TODO: Add a check to ensure player_id is valid
        self.playerID = player_id

    def set_player_hand(self, hand: Hand):
        self.playerHand = hand

    def set_eliminated(self, val: bool = True):
        self._eliminated = True

    def is_eliminated(self) -> bool:
        return self._eliminated

    def __str__(self):
        return self._character
