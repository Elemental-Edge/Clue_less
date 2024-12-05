
from __future__ import annotations
from Backend.cardGroupings.Card import Card
#from Backend.gameboardGroupings.space import Space, SpaceType
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

    def get_player_ID(self):
        return self.playerID
    
    def is_eliminated(self):
        return self.isEliminated

    def get_character_name(self):
        return self.character
    
    def set_player_eliminated(self, isEliminated: bool):
        self.isEliminated = isEliminated

    def receive_card_dealt(self, card: Card):
        self.playerHand.add_card(card)

    def get_valid_moves(self) -> list['Space']:
        # returns a list of Space objects
        adj: list['Space'] = self.currLocation.get_adjacent_spaces()

        possible_dest = []
        # check if adjacent spaces are empty
        for sp in adj:
            if SpaceType.HALLWAY == sp.get_space_type():
                if sp.is_empty():
                    possible_dest.append(sp)
            else:
                possible_dest.append(sp)
        return possible_dest
    


