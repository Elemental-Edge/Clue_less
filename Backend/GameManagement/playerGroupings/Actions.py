
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional

from Backend.GameManagement.playerGroupings.player import Player
from Backend.gameboardGroupings.turn_order import TurnOrder
from Backend.cardGroupings.Card import Card, CardType
from Backend.cardGroupings.Hand import Hand
from Backend.gameboardGroupings.space import SpaceType,Space

class Actions():
    def __init__(self, player: 'Player', playerTurn: 'Player_Turn'):
        from Backend.GameManagement.playerGroupings.player_turn import Player_Turn
        p : 'Player' = player
        pt : 'Player_Turn' = playerTurn


class Accusation(Actions) :

    def __init__(self, player: Player, playerTurn: 'Player_Turn', aCaseFile: 'Hand'):
        super().__init__(player, playerTurn)
        self.case_file = aCaseFile

    def makeAccusation(self, aSuspect: str, aWeapon: str, aRoom: str) -> bool:
        """
        Checks if the accusation made by the user was correct.

        Attributes:
            aSuspect (str): Represents cards that depict suspects involved in the game.
            aRoom (str): Represents cards that indicate various locations or rooms.
            aWeapon (str): Represents cards that depict weapons that can be used in the game.
        """

        suspect = Card(aSuspect, card_type = CardType.SUSPECT)
        weapon = Card(aWeapon, card_type=CardType.WEAPON)
        room = Card(aRoom, card_type=CardType.ROOM)

        # Check if accusation hands matches the case file
        return ( self.case_file.has_card(suspect)
            and self.case_file.has_card(weapon)
            and self.case_file.has_card(room))

class Suggestion(Actions):
    def __init__(self, aPlayer: 'Player', aTurnOrder: 'TurnOrder'):
        super().__init__(aPlayer)
        self.turnOrder = aTurnOrder

    def makeSuggestion(self, aSuspect: str, aWeapon: str, aRoom: str) -> tuple['Player', 'Hand']:
        """
        Checks if the accusation made by the user was correct.

        Attributes:
            aSuspect (str): Represents cards that depict suspects involved in the game.
            aRoom (str): Represents cards that indicate various locations or rooms.
            aWeapon (str): Represents cards that depict weapons that can be used in the game.
        """
        suggestedCards = Hand()
        suggestedCards.add_card(Card(aSuspect, card_type = CardType.SUSPECT))
        suggestedCards.add_card(Card(aWeapon, card_type=CardType.WEAPON))
        suggestedCards.add_card(Card(aRoom, card_type=CardType.ROOM))

        #TODO: Update turnOrder to Circular List
        turnList_iter = iter(self.turnOrder)
        nextPlayer: Optional['Player'] = None
        if (None != self.p):
            raise ValueError("Current Player not defined! :-(")
        # output list of player's cards that match suggestion
        disproveCards = Hand()
        nextPlayer = next(turnList_iter)
        while (nextPlayer != self.p):
            if (None == nextPlayer):
                break
            if (nextPlayer.isEliminated):
                continue
            # Check player's hand for matching cards
            for card in suggestedCards.get_hand():
                if (nextPlayer.playerHand.hand.has_card(card)):
                    disproveCards.add_card(card)

            if (not disproveCards.isEmpty()):
                break
            nextPlayer = next(turnList_iter)
        return (nextPlayer, disproveCards)

class Move(Actions):

    def __init__(self, player: Player, playerTurn: 'Player_Turn'):
        super().__init__(player, playerTurn)

    def makeMove(self, aDest: 'Space') -> bool:

        if None == aDest:
            return False
        # if (SpaceType.HALLWAY == aDest.get_space_type()):
        #     return False

        # Check if Destination is in Adjacent Spaces
        if not aDest in self.p.currLocation.get_adjacent_spaces():
            return False
        # have player select a move
        selected_destination = aDest

        if(selected_destination.get_space_type() == SpaceType.ROOM):
            self.pt.hasEnteredRoom = True

        selected_destination.add_player(self.p)

        self.p.prevLocation = self.p.currLocation
        self.p.currLocation.remove_player(self.p)

        self.p.currLocation = selected_destination

        # TODO: broadcast move
        return True
