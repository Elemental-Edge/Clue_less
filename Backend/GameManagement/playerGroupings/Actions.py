from __future__ import annotations
from abc import abstractmethod
from Backend.gameboardGroupings.turn_order import TurnOrder

from Backend.cardGroupings.Card import Card, CardType
from Backend.cardGroupings.Hand import Hand
from Backend.gameboardGroupings.space import SpaceType, Space


class Actions:
    def __init__(self, aTurnOrder: TurnOrder):

        self._turn_order: TurnOrder = aTurnOrder

    def get_player(self):
        return self._turn_order.get_current_turn()

    @abstractmethod
    def __str__(self):
        pass


class Accusation(Actions):

    def __init__(self, aTurnOrder, aCaseFile: Hand):
        super().__init__(aTurnOrder)
        self._case_file = aCaseFile

    def makeAccusation(self, aSuspect: str, aWeapon: str, aRoom: str) -> bool:
        """
        Checks if the accusation made by the user was correct.

        Attributes:
            aSuspect (str): Represents cards that depict suspects involved in the game.
            aRoom (str): Represents cards that indicate various locations or rooms.
            aWeapon (str): Represents cards that depict weapons that can be used in the game.
        """
        if None is self._turn_order:
            raise ValueError("Turn Order Object is None: No Players in Turn Order")

        if None is self._case_file:
            raise ValueError("Case File Object is NULL")

        suspect = Card(aSuspect, card_type=CardType.SUSPECT)
        weapon = Card(aWeapon, card_type=CardType.WEAPON)
        room = Card(aRoom, card_type=CardType.ROOM)

        self.get_player().get_player_turn().set_hasMadeAccusation()

        # Check if accusation hands matches the case file
        return (
            self._case_file.has_card(suspect)
            and self._case_file.has_card(weapon)
            and self._case_file.has_card(room)
        )

    def __str__(self):
        return "accusation"


class Suggestion(Actions):

    def __init__(self, aTurnOrder):
        super().__init__(aTurnOrder)

    def makeSuggestion(
        self, aSuspect: str, aWeapon: str, aRoom: str, aRoomSpace: "Space"
    ) -> tuple["Player", list[str]]:
        """
        Checks if the accusation made by the user was correct.

        Attributes:
            aSuspect (str): Represents cards that depict suspects involved in the game.
            aRoom (str): Represents cards that indicate various locations or rooms.
            aWeapon (str): Represents cards that depict weapons that can be used in the game.
        """

        if None is self._turn_order:
            raise ValueError("Turn Order Object is None: No Players in Turn Order")

        suggestedCards = Hand()
        suggestedCards.add_card(Card(aSuspect, card_type=CardType.SUSPECT))
        suggestedCards.add_card(Card(aWeapon, card_type=CardType.WEAPON))
        suggestedCards.add_card(Card(aRoom, card_type=CardType.ROOM))

        self._turn_order.update_suggested_player(aSuspect, aRoomSpace)
        # output list of player's cards that match suggestion
        disproveCards = Hand()
        # nextPlayer = next(turnList_iter)
        first_run: bool = True
        disprove_Player: "Player" | None = None
        for player in self._turn_order:
            print(f"player {player.get_character()} ")
            if None is player:
                break
            if first_run and player == self.get_player():
                continue
            first_run = False
            if player.is_eliminated():
                continue
            # Check player's hand for matching cards
            for card in suggestedCards.get_hand():
                if player.get_hand().has_card(card):
                    disproveCards.add_card(card)
                    disprove_Player = player
                    print(f"disprove_player is {disprove_Player.get_character()}")

            if not disproveCards.isEmpty():
                break

        toReturnDisproveCardsList = []
        for el in disproveCards.get_hand():
            toReturnDisproveCardsList.append(el.get_name())
        self.get_player().get_player_turn().set_hasMadeSuggestion()
        return disprove_Player, toReturnDisproveCardsList

    def __str__(self):
        return "suggestion"


class Move(Actions):

    def __init__(self, aTurnOrder):
        super().__init__(aTurnOrder)

    def makeMove(self, aDest: Space) -> bool:

        if None is aDest:
            raise ValueError("Empty Destination Object Case File")

        current_player = self.get_player()
        currentLocation = current_player.get_current_location()
        if None is currentLocation:
            return False
        # Check if Destination is in Adjacent Spaces
        if aDest not in currentLocation.get_adjacent_spaces():
            return False
        # have player select a move
        selected_destination = aDest

        if selected_destination.get_space_type() == SpaceType.ROOM:
            current_player.get_player_turn().set_hasEnteredRoom()

        retVal = current_player.set_current_location(selected_destination)
        if not retVal:
            return False
        self.get_player().get_player_turn().set_hasMoved()
        return True

    def __str__(self):
        return "move"
