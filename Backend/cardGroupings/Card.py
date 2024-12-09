from __future__ import annotations
from enum import Enum
from Backend.commons import ValidRooms, ValidSuspect, ValidWeapons


class CardType(Enum):
    """
    An enumeration representing the various types of cards in a game.

    This enumeration categorizes the types of cards that can be used during the game.

    Attributes:
        SUSPECT (CardType): Represents cards that depict suspects involved in the game.
        ROOM (CardType): Represents cards that indicate various locations or rooms.
        WEAPON (CardType): Represents cards that depict weapons that can be used in the game.
    """

    SUSPECT = "Suspect"
    ROOM = "Room"
    WEAPON = "Weapon"


class Card:
    """
    Class object to represent valid card types in the game clue-less.

    Attributes:
        VALID_SUSPECTS: List of valid suspect
        VALID_WEAPONS: List of valid weapons
        VALID_ROOMS: List of valid rooms
    """

    def __init__(self, name: str, card_type: CardType):
        if card_type == CardType.SUSPECT and name not in [character.value for character in ValidSuspect]:
            raise ValueError(f"{name} is not a valid suspect.")
        elif card_type == CardType.WEAPON and name not in [weapon.value for weapon in ValidWeapons]:
            raise ValueError(f"{name} is not a valid weapon.")
        elif card_type == CardType.ROOM and name not in [room.value for room in ValidRooms]:
            raise ValueError(f"{name} is not a valid room.")

        self._name = name
        self._card_type = card_type

    def get_name(self) -> str:
        return self._name

    def get_card_type(self) -> CardType:
        return self._card_type

    # Compare function
    def __eq__(self, other) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self._name == other._name and self._card_type == other._card_type

    # Less than Function : Used for sorting
    def __lt__(self, other):
        if not isinstance(other, Card):
            return NotImplemented

        # Compare by card_type first, then by name
        if self._card_type == other.get_card_type():
            return self._name < other.get_name()
        return self._card_type.value < other.get_card_type().value

    def __repr__(self) -> str:
        return f"Card(name='{self._name}', card_type={self._card_type})"

    def __str__(self) -> str:
        return self._name


if __name__ == "__main__":
    card1 = Card(ValidSuspect.GREEN, CardType.SUSPECT)
    card2 = Card(ValidRooms.DINING, CardType.ROOM)
    card3 = Card(ValidWeapons.DAGGER, CardType.WEAPON)

    print(card1)
    print(card2)
    print(card3)

    # Comparing cards
    card4 = Card(ValidSuspect.GREEN, CardType.SUSPECT)
    print(card1 == card4)  # Output: True
    print(card1 == card2)  # Output: False
