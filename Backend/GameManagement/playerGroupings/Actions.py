
from abc import ABC, abstractmethod

import Backend
from Backend.GameManagement.player import Player
from Backend.GameManagement.player_turn import Player_Turn
from Backend.GameManagement.gameboardGrouping import game_board, game_processor, space
from Backend.cardGroupings import Card, Deck, Hand, CardType

class Actions():
    p: Player
    pt: Player_Turn

    def __init__(self, player: Player, playerTurn: Player_Turn):
        p = player
        pt = playerTurn

    @abstractmethod
    def validate(self):

    @abstractmethod
    def perform_action(self):


class Accusation(Actions):
    suspect: str
    weapon: str
    room: str

    def validate(self):
        return self.pt.hasMadeAccusation

    def perform_action(self, deck: Deck):
        # enter checking win conditions
        winningCards_iter = iter(list(Backend.GameManagement.GameProcessor.winningCards))
        nextCard = next(winningCards_iter)

        # output to GUI/client list of options for suspect, have them choose one

        self.suspect = selected_suspect

        # output to GUI/client list of options for weapon, have them choose one

        self.weapon = selected_weapon

        # output to GUI/client list of options for room, have them choose one

        self.room = selected_room

        suspectCorrect = False
        weaponCorrect = False
        roomCorrect = False

        # loop
        # use has_card() from Hand to check membership of winningHand/case_file
        case_file.has_card(self.suspect)
        case_file.has_card(self.weapon)
        case_file.has_card(self.room)

        if (suspectCorrect and weaponCorrect and roomCorrect):
            # player wins game, enter win game state
        else:
            # output player eliminated
            p.isEliminated = True

class Suggestion(Actions):
    suspect: str
    weapon: str
    room: str

    def validate(self):
        if self.pt.hasEnteredRoom:
            if not self.pt.hasMadeAccusation and not self.pt.hasMadeSuggestion:
                return True
        return False

    def perform_action(self):
        # prompt for susepct, weapon, room

        self.create_suggestion(suspect, weap, room_suggest)

        disproveFinished = False

        turnList = Backend.GameManagement.GameProcessor.turnOrder
        turnList_iter = iter(turnList)
        nextPlayer = None
        while (nextPlayer != p):
            nextPlayer = next(turnList_iter)

            while(not disproveFinished):
                # ask player to disprove
                # output list of player's cards that match suggestion
                disproveCards = []
                for card in self.p.playerHand:
                    curr_card = card.get_name()
                    if curr_card == self.suspect or curr_card == self.weapon or curr_card == self.room:
                        disproveCards.append(curr_card)

                if not disproveCards:
                    return False
                else:
                    # have them select one
                    # wait for them to accept then broadcast event (not card)
                    disproveFinished = True

        self.pt.hasMadeSuggestion = True


    def create_suggestion(self, suspect: str, weap: str, room_suggest: str):
        # change to card instead of String
        self.suspect = suspect
        self.weapon = weap
        self.room = room_suggest

        # move player and weapon tokens to the room suggested
        Player susp = game_processor.get_player_associated_with_character(self.suspect)
        game_processor.move_player(susp, self.room)


class Move(Actions):

    def validate(self):
        if self.p.get_valid_moves():
            return True
        return False

    def perform_action(self):
        moves_list = self.p.get_valid_moves()

        # output possible moves
        adj = self.p.currLocation.get_adjacent_spaces()

        possible_dest = []
        # check if adjacent spaces are empty
        for sp in adj:
            if sp.is_empty():
                possible_dest.append(sp)

        # have player select a move
        selected_destination

        if(selected_destination.get_space_type() == ROOM):
            self.pt.hasEnteredRoom = True

        selected_destination.add_player(self.p)
        self.p.currLocation.remove_player(self.p)

        # broadcast move






