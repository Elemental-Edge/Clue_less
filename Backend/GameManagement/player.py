
import Backend.cardGroupings.Card

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
        adj = self.currLocation.adjacentSpaces
        returnList = []
        for Space s in adj:
            if s.isEmpty:
                returnList.append(s)

        return returnList


