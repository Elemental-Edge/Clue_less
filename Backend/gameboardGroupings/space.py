from __future__ import annotations
from enum import Enum, auto
from typing import List
from GameManagement.player import Player

SPACE_NAME = ""
CREATE_BIDIRECTIONAL_CONN = True


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
        return self.name.replace("_", " ").tite()


class Space:
    def __init__(self, name: str = SPACE_NAME):
        self._name: str = name
        self._space_type: SpaceType = None
        self._players: List[Player] = []
        self._adjacent_spaces: List[Space] = []
        self._player_count: int = 0

    def __eq__(self, other: object) -> bool:
        """Overloads the equal operator and establishes that two spaces are
        equal if both spaces have the same space type, name (rooms), or
        same adjacent spaces(hallways)."""
        if not isinstance(other, Space):
            return False
        if self._space_type != other._space_type:
            return False
        if self._space_type == SpaceType.HALLWAY:
            return self._adjacent_spaces == other._adjacent_spaces
        return self._name == other._name

    def get_player_count(self) -> int:
        """Returns the number of players in the space."""
        return self._player_count

    def get_players(self) -> List[Player]:
        """Reutnrs list of players in the space."""
        return self._players

    def get_adjacent_spaces(self) -> List[Space]:
        """Returns list of adjacent spaces"""
        return self._adjacent_spaces

    def get_space_type(self) -> int:
        """Returns an integer value that represents the space type."""
        return self._space_type

    def add_adjacent_space(self, space: Space, create_bidirectional: bool = CREATE_BIDIRECTIONAL_CONN) -> None:
        """Adds a space to adjacent spaces list and creates reciprocal connection by default""" 
        if create_bidirectional:
            space._adjacent_spaces.append(self)

        self._adjacent_spaces.append(space)
    
    def add_player(self, player: Player):
        """Adds a player to the space"""
        if not self.is_player_in_room(player):
            self._players.append(player)
            self._player_count += 1

    
    def is_player_in_room(self, player_id: int) -> bool:
        """Returns True if the player's associated ID is found in the players
           list, otherwise the function Returns False."""
        in_room = False
        for _player in self._players:
            if _player.playerID == player_id:
                in_room = True
                break
        return in_room


    def remove_player(self, player_id: int) -> bool:
        """Removes a player from the space, based on the player's associated ID
           number."""
        player_index = self.get_player_index(player_id)
        is_success = False
        if player_index != -1:
            del self._players[player_index]
            self._player_count -= 1
            is_success = True
        return is_success
    
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
