
from Backend.GameManagement.Actions import Actions, Suggestion, Accusation, Move
from Backend.GameManagement.player import Player
from Backend.GameManagement.gameboardGrouping import game_board, game_processor, space
from Backend.cardGroupings import Card, Deck, Hand

class Player_Turn():
    p: Player
    isActive: bool
    hasMadeAccusation: bool
    hasMadeSuggestion: bool
    hasEnteredRoom: bool
    hasMoved: bool

    def __init__(self, player: Player):
        p = player
        self.isActive = False
        self.hasMadeAccusation = False
        self.hasMadeSuggestion = False
        self.hasEnteredRoom = False
        self.hasMoved = False

    # isActive becomes True only when get_valid_actions() is called
    def get_valid_actions(self):
        return_list = []
        self.isActive = True
        if self.hasEnteredRoom and not self.hasMadeSuggestion:
            return_list.append(Suggestion(self.p, self))
        if not self.hasMadeAccusation:
            return_list.append(Accusation(self.p, self))
        if not self.hasMoved:
            return_list.append(Move(self.p, self))
        return return_list

    def take_action(self, action: Actions):
        action.perform_action()

    def end_turn(self):
        self.isActive = False
        self.hasMadeAccusation = False
        self.hasMadeSuggestion = False
        self.hasEnteredRoom = False
        self.hasMoved = False

