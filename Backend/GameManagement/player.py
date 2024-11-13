
from Backend.cardGroupings.Card import Card
import Backend.GameManagement.gameboardGrouping
from Backend.GameManagement.gameboardGrouping.space import Space, SpaceType

class Player():
    playerName: str
    playerID: int
    character: str
    playerHand: list
    currLocation: Space
    prevLocation: Space
    isEliminated: bool

    def __init__(self, name: str):
        self.playerName = name
        self.isEliminated = False

    def receive_card_dealt(self, card: Card):
        self.playerHand.add_card(card)

    def get_valid_moves(self):
        # returns a list of Space objects
        adj = self.currLocation.adjacent_spaces()
        returnList = []
        for s in adj:
            if s.get_space_type() == SpaceType.HALLWAY and is_instance(s, Hallway) and s.is_empty():
                h =
                returnList.append(s)

        return returnList


