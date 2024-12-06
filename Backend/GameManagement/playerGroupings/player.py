
from __future__ import annotations
from Backend.cardGroupings.Card import Card
from Backend.cardGroupings.Hand import Hand
from Backend.cardGroupings.Card import Card

class Player():
    playerName: str
    playerID: int
    character: str
    playerHand: Hand
    currLocation: 'Space'
    prevLocation: 'Space'
    isEliminated: bool

    def __init__(self, name: str):
        self.playerName = name
        self.isEliminated = False

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
    
    def get_hand(self) -> Hand:
        return self.playerHand
    
    def get_character(self) -> str:
        return self.character
    
    def get_current_location(self) -> 'Space':
        return self.currLocation

    def set_current_location(self, sp: 'Space'):
        self.currLocation = sp
    
    def is_eliminated(self) -> bool:
        return self.isEliminated
    
    def __str__(self):
        return self.character



