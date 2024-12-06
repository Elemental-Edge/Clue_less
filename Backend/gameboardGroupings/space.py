from __future__ import annotations
from enum import Enum, auto
from typing import List
from Backend.GameManagement.playerGroupings.player import Player
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
        return self.name.replace("_", " ").titegit()

class Space:
    def __init__(self, name: str = SPACE_NAME):
        self._name: str = name
        self._space_type: SpaceType = None
        self._players: List['Player'] = []
        self._adjacent_spaces: List[Space] = []
        # represents all spaces adjacent to the space
        self._player_count: int = 0
        # stores player count to prevent constant calls to len() to get
        # _players list length

    def __eq__(self, other: object) -> bool:
        return self is other

    def get_player_count(self) -> int:
        """Returns the number of players in the space."""
        return self._player_count

    def get_players(self) -> List[Player]:
        """Returns list of players in the space."""
        return self._players

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

    def add_player(self, player: Player) -> bool:
        """Adds a player to the space"""
        is_success = False
        if not self.is_player_in_room(player):
            self._players.append(player)
            self._player_count += 1
            is_success = True
        return is_success


    def is_player_in_room(self, player_id: int) -> bool:
        """Returns True if the player's associated ID is found in the players
        list, otherwise the function Returns False."""
        in_room = False
        for player in self._players:
            if player.playerID == player_id:
                in_room = True
                break
        return in_room

    def remove_player(self, player_id: int) -> Player | None:
        """Removes a player from the space, based on the player's associated ID
        number."""
        # change function to take a player object
        player_index = self.get_player_index(player_id)
        player = None
        if player_index != -1:
            player = self._players.pop(player_index)
            self._player_count -= 1
        return player

    def get_player_index(self, player_id: int) -> int:
        """Gets a player index based on the playerID"""
        current_index = 0
        is_found = False
        while current_index < self._player_count and not is_found:
            if self._players[current_index].playerID == player_id:
                is_found = True
            else:
                current_index += 1
        if not is_found:
            current_index = -1
        return current_index

    def clear_players(self):
        """Clears players list in the space and sets player count to 0"""
        self._players.clear()
        self._player_count = 0

    def get_player_by_id(self, player_id: int) -> Player | None:
        """Gets the player associated with a player id"""
        found_player = None
        for player in self._players:
            if player.playerID == player_id:
                found_player = player
                break
        return found_player

    def get_player_by_character(self, character_name: str) -> Player | None:
        """Gets the player associated with a specific character name"""
        found_player = None
        for player in self._players:
            if player.character == character_name:
                found_player = player
                break
        return found_player


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
        self._current_player = None

    def is_empty(self) -> bool:
        """Returns True if no players are in the hallway"""
        return self._current_player is None

    def add_player(self, player: Player) -> bool:
        """Overrides the base class function to add a player. Only adds
        a player if the hallway is empty."""
        is_success = False
        if self.is_empty():
            self._current_player = player
            is_success = True
        return is_success
