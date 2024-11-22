from enum import Enum, auto
from typing import List, Optional, Union, Set
from player import Player


class SpaceType(Enum):
    """Represents different types of spaces on the game board."""
    ROOM = auto()
    CORNER_ROOM = auto()
    HALLWAY = auto()

    def __str__(self) -> str:
        return self.name.replace('_', ' ').title()


class Space:
    """Base class for all spaces on the game board."""
    
    def __init__(self, name: str = ""):
        self.name: str = name
        self.space_type: SpaceType = None
        self._players: Set[Player] = set()  # Using set for O(1) lookups
        self._adjacent_spaces: Set[Space] = set()  # Using set for O(1) lookups
        self.player_count: int = 0

    def __eq__(self, other: object) -> bool:
        """Two spaces are equal if they have the same type and either same name (rooms) 
        or same adjacent spaces (hallways)."""
        if not isinstance(other, Space):
            return False
        if self.space_type != other.space_type:
            return False
        if self.space_type == SpaceType.HALLWAY:
            return self._adjacent_spaces == other._adjacent_spaces
        return self.name == other.name

    def __hash__(self) -> int:
        """Hash based on space type and either name or adjacent spaces."""
        if self.space_type == SpaceType.HALLWAY:
            # Sort room names for consistent hashing
            connected_rooms = tuple(sorted(
                space.name for space in self._adjacent_spaces 
                if space.space_type != SpaceType.HALLWAY
            ))
            return hash((self.space_type, connected_rooms))
        return hash((self.space_type, self.name))

    def player_count(self) -> int:
        """Returns number of players in the space."""
        return self.player_count

    def players(self) -> List[Player]:
        """Returns list of players in the space."""
        return list(self._players)

    def adjacent_spaces(self) -> List[Space]:
        """Returns list of adjacent spaces."""
        return list(self._adjacent_spaces)
    
    def get_space_type(self) -> int:
        return self.space_type

    def add_adjacent_space(self, space: Space) -> None:
        """
        Adds a space to adjacent spaces and creates reciprocal connection.
        
        Args:
            space: Space to add as adjacent
            
        Raises:
            ValueError: If space is invalid or would create invalid connection
        """
        if space is self:
            raise ValueError("Space cannot be adjacent to itself")
            
        if self.space_type == SpaceType.HALLWAY:
            # Validate hallway connections
            room_connections = sum(1 for s in self._adjacent_spaces 
                                 if s.space_type != SpaceType.HALLWAY)
            if room_connections >= 2:
                raise ValueError("Hallway cannot connect to more than two rooms")
            if space.space_type == SpaceType.HALLWAY:
                raise ValueError("Hallways cannot connect to other hallways")

        # Add bidirectional connection
        self._adjacent_spaces.add(space)
        space._adjacent_spaces.add(self)

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the space.
        
        Args:
            player: Player to add
            
        Raises:
            ValueError: If player is already in space
        """
        if player in self._players:
            raise ValueError(f"Player {player} is already in this space")
        self._players.add(player)
        self.player_count += 1

    def remove_player(self, player: Player) -> None:
        """
        Removes a player from the space.
        
        Args:
            player: Player to remove
            
        Raises:
            ValueError: If player is not in space
        """
        if player not in self._players:
            raise ValueError(f"Player {player} is not in this space")
        self._players.remove(player)

    def clear_players(self) -> None:
        """Removes all players from the space."""
        self._players.clear()

class Room(Space):
    """Represents a room in the game."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.space_type = SpaceType.ROOM
        self._secret_passages: Set[Room] = set()
        self._weapons: Set[Weapon] = set()

    def secret_passages(self) -> List[Room]:
        """Returns list of rooms connected by secret passages."""
        return list(self._secret_passages)

    def weapons(self) -> List[Weapon]:
        """Returns list of weapons in the room."""
        return list(self._weapons)

    def add_secret_passage(self, room: Room) -> None:
        """
        Adds a secret passage to another room.
        
        Args:
            room: Room to connect via secret passage
            
        Raises:
            ValueError: If connection would be invalid
        """
        if not isinstance(room, Room):
            raise ValueError("Secret passages can only connect to rooms")
        if room is self:
            raise ValueError("Cannot create secret passage to self")
        
        self._secret_passages.add(room)
        room._secret_passages.add(self)

    def add_weapon(self, weapon: Weapon) -> None:
        """Adds a weapon to the room if not already present."""
        self._weapons.add(weapon)

    def remove_weapon(self, weapon: Weapon) -> None:
        """
        Removes a weapon from the room.
        
        Raises:
            ValueError: If weapon is not in room
        """
        if weapon not in self._weapons:
            raise ValueError(f"Weapon {weapon} is not in this room")
        self._weapons.remove(weapon)

    def has_secret_passage(self) -> bool:
        """Returns whether room has any secret passages."""
        return bool(self._secret_passages)


class CornerRoom(Room):
    """Represents a corner room in the game."""
    
    def __init__(self, name: str):
        super().__init__(name)
        self.space_type = SpaceType.CORNER_ROOM


class Hallway(Space):
    """
    Represents a hallway space in the game.
    Can only hold one player and must connect exactly two rooms.
    """
    
    def __init__(self):
        super().__init__("")  # Hallways don't need names
        self.space_type = SpaceType.HALLWAY
        self._must_leave = False

    def is_empty(self) -> bool:
        """Returns whether hallway has no players."""
        return self.player_count == 0

    def must_leave(self) -> bool:
        """Returns whether players must leave this hallway."""
        return self._must_leave

    def set_must_leave(self, value: bool) -> None:
        self._must_leave = value

    def add_player(self, player: Player) -> None:
        """
        Adds a player to the hallway if empty.
        
        Args:
            player: Player to add
            
        Raises:
            ValueError: If hallway is occupied
        """
        if not self.is_empty:
            connected_rooms = [s.name for s in self._adjacent_spaces 
                             if s.space_type != SpaceType.HALLWAY]
            raise ValueError(
                f"Cannot add player to hallway between {' and '.join(connected_rooms)}: "
                "hallway is occupied"
            )
        super().add_player(player)
        super().player_count += 1

    def connected_rooms(self) -> List[str]:
        """Returns names of rooms this hallway connects."""
        return sorted(
            space.name for space in self._adjacent_spaces 
            if space.space_type != SpaceType.HALLWAY
        )