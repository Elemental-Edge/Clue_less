from __future__ import annotations
from enum import Enum, auto
from typing import List
from Backend.cardGroupings.Card import CardType, Card

SPACE_NAME = ""


class SpaceType(Enum):
    """Enum that Represents the different types of spaces on the game board."""

    ROOM = auto()
    CORNER_ROOM = auto()
    HALLWAY = auto()

    def __str__(self) -> str:
        """Calling the str() function on the SpaceType enum returns a string
        that represents the room type.
        """
        # Returns the SpaceType Name
        return self.name.replace("_", " ").title()


class Space:
    def __init__(self, name: str = SPACE_NAME):
        """Constructor initializes the class."""
        self._name: str = name
        self._space_type: SpaceType = None
        self._adjacent_spaces: List[Space] = []
        # represents all spaces adjacent to the space
        self._player_count: int = 0
        # stores player count to prevent constant calls to len() to get
        # _players list length

    def __eq__(self, other: object) -> bool:
        """Overloads the equality operator to check for space equality via
           memory address comparison"""
        return self is other

    def get_player_count(self) -> int:
        """Returns the number of players in the space."""
        return self._player_count

    def get_adjacent_spaces(self) -> List[Space]:
        """Returns list of adjacent spaces"""
        return self._adjacent_spaces

    def get_space_type(self) -> int:
        """Returns an integer value that represents the space type."""
        return self._space_type

    def add_adjacent_space(self, space: Space):
        """Adds a space to adjacent spaces list and creates reciprocal
           connection by default"""
        if space is not self:
            space._adjacent_spaces.append(self)
            self._adjacent_spaces.append(space)
        else:
            raise ValueError(f"{space._name} cannot be adjacent to itself")

    def remove_adjacent_space(self, space_name: str) -> Space | None:
        """"""
        removed_space = self.get_adjacent_space(space_name)
        if removed_space is not None:
            removed_space.remove_adjacent_space(self._name)
        return removed_space

    def get_adjacent_space(self, space_name: str) -> Space | None:
        space_index = self.get_adjacent_space_index(space_name)
        space = None
        if space_index != -1:
            space = self._adjacent_spaces.pop(space_index)

        return space

    def get_adjacent_space_index(self, space_name: str) -> int:
        current_index = 0
        is_found = False
        spaces_count = len(self._adjacent_spaces)
        while current_index < spaces_count and not is_found:
            if self._adjacent_spaces[current_index]._name == space_name:
                is_found = True
            else:
                current_index += 1
        if not is_found:
            current_index = -1
        return current_index

    def is_adjacent_room(self, space_name: str) -> bool:
        is_room = False
        for space in self._adjacent_spaces:
            if space._name == space_name:
                is_room = True
                break
        return is_room

    def add_player_count(self):
        """increments the player count in the space."""
        self._player_count += 1

    def remove_player_count(self):
        """decrements the player count in the space."""
        self._player_count -= 1
    
    def is_empty(self) -> bool:
        return self._player_count == 0


class Room(Space):
    """Represents a standard room on a game board"""

    def __init__(self, name: str):
        super().__init__(name)
        self._space_type: SpaceType = SpaceType.ROOM
        self._weapons: List[Card] = []
        self._weapon_count: int = 0

    def get_weapons(self) -> List[Card] | None:
        """Returns a list of weapons in the room or None, if no
        weapon is found in the room"""
        return self._weapons

    def add_weapon(self, weapon: Card):
        """Adds a weapon to the room"""
        if weapon.get_card_type() == CardType.WEAPON:
            self._weapons.append(weapon)
        else:
            raise ValueError("Card is not type Weapon")

    def remove_weapon(self, weapon_name: str) -> Card | None:
        """Removes a weapon from the room and returns it"""
        weapon_index = self.get_weapon_index(weapon_name)
        weapon = None
        if weapon_index != -1:
            weapon = self._weapons.pop(weapon_index)
        return weapon

    def get_weapon_index(self, weapon_name: str) -> int:
        """Gets a player index based on the playerID"""
        current_index = 0
        is_found = False
        while current_index < self._weapon_count and not is_found:
            if self._weapons[current_index].get_name == weapon_name:
                is_found = True
            else:
                current_index += 1
        if not is_found:
            current_index = -1
        return current_index


class CornerRoom(Room):
    def __init__(self, name: str):
        super().__init__(name)
        self._secret_passage: CornerRoom = None
        self._space_type = SpaceType.CORNER_ROOM

    def get_secret_passage(self) -> CornerRoom | None:
        """Returns a list of secret passages"""
        return self._secret_passage

    def add_secret_passage(self, secret_passage: CornerRoom):
        """Adds a secrete passage to the room"""
        if secret_passage is not self:
            self._secret_passage = secret_passage
            secret_passage._secret_passage = self
        else:
            raise ValueError(f"{self._name} cannot be adjacent to itself")

    def remove_secret_passage(self) -> CornerRoom | None:
        removed_room = None
        if self.has_secret_passage():
            removed_room = self._secret_passage
            removed_room._secret_passage = None
            self._secret_passage = None
        return removed_room

    def has_secret_passage(self) -> bool:
        """Returns True if the Room has a secret passage"""
        return self._secret_passage is not None


class Hallway(Space):
    """Represents a hallway space in the game. Can only hold one player"""

    def __init__(self, name: str = SPACE_NAME):
        super().__init__(name)  # Hallways don't need names
        self._space_type = SpaceType.HALLWAY
