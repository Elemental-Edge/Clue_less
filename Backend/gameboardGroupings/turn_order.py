from typing import List
from random import shuffle
from typing import Iterator
from Backend.GameManagement.playerGroupings.player import Player
from Backend.commons import ValidSuspect


class Node:
    """A node in the circular singly circular linked list. Stores the
    reference to Player Object and the next Player in
    the singly circular linked list"""

    def __init__(self, player: Player):
        self.player = player  # Player this node represents
        self.next = None  # Pointer to the next node


class TurnOrder:
    """Manages the turn order using a circular singly linked list."""

    def __init__(self):
        self._head = None  # First node in the list
        self._tail = None  # Last node in the list
        self._current = None  # Current player's turn
        self._size = 0

    def add_player(self, player: Player):
        """
        Add a player to the turn order.
        Creates a new node for the player and appends it to the end of the circular list.
        """
        new_node = Node(player)
        if self._head is None:
            # First player in the list
            self._head = new_node
            self._tail = new_node
            new_node.next = new_node  # Circular reference
            self._current = new_node
            self._size += 1
        else:
            # Append the new node at the end
            self._tail.next = new_node
            new_node.next = self._head
            self._tail = new_node
            self._size += 1

    def remove_player(self, player_id: int) -> None | Player:
        """
        Remove a player from the turn order.
        Traverses the list to find the player and removes their node.
        If the player is the only one, clears the list.
        """
        if self._head:
            prev = self._tail
            current = self._head
        else:  # no active players
            return None

        first_run: bool = True
        while first_run or current != self._head:  # Traverse until full cycle
            first_run = False
            if current.player.get_playerID() == player_id:
                if current == self._head and current == self._tail:
                    # Only one player in the list
                    self._head = None
                    self._tail = None
                    self._current = None
                    self._size -= 1
                else:
                    # Update links to remove the node
                    prev.next = current.next
                    if current == self._head:
                        self._head = current.next
                        self._size -= 1
                    elif current == self._tail:
                        self._tail = prev
                        self._size -= 1
                    else:
                        self._current = prev.next
                        self._size -= 1

                return current.player  # Return the removed player
            prev = current
            current = current.next
        return None  # Player not found

    def get_current_turn(self) -> Player:
        """
        Get the player whose turn it is.
        Returns the player at the `current` node.
        """
        return self._current.player if self._current else None

    def advance_turn(self):
        """
        Move to the next player's turn.
        Updates the `current` pointer to the next node in the list.
        """
        if self._current:
            for node in self.get_node():
                if node.player == self._current.player:
                    continue
                if node.player.get_active():
                    self._current = node
                    self.reset_player_turn()
                    break
    
    def get_node(self) -> Iterator[Player] | None:
        if not self._head:
            return None

        current = self._current
        first_iteration = True

        while None is not current and (first_iteration or current != self._current):
            yield current  # Yield the player at the current node
            current = current.next
            first_iteration = False  # After the first iteration, we set this to False
        
        return 

    def reverse_order(self):
        """
        Reverse the order of players in the turn order.
        Reverses the direction of the `next` pointers and updates the `head` and `tail`.
        """
        if self._head is None or self._head.next == self._head:
            return  # No players or only one player

        prev = self._tail
        current = self._head
        first_node = self._head

        while current != first_node or prev == self._tail:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        # Update head and tail and reconnect the circular link
        self._tail = self._head
        self._head = prev
        self._tail.next = self._head
        self._current = self._head

    def randomize_order(self):
        """
        Randomize the turn order of players.
        Collects all players into a list, shuffles the list, and rebuilds the circular linked list.
        """
        if self._head is None or self._head.next == self._head:
            return  # No players or only one player

        # Collect all players
        players = self.get_turn_order()

        # Shuffle the list of players
        shuffle(players)

        # Rebuild the circular list
        self._head = None
        self._tail = None
        self._current = None
        for player in players:
            self.add_player(player)

    def get_turn_order(self, getAll: bool = False) -> List[Player]:
        """
        Get a list of players in the current turn order.
        Traverses the circular list and collects all players in order.
        """
        players = []
        if self._head is None:
            return players

        for current_player in self:
            if current_player.get_active() or getAll:
                players.append(current_player)
        return players

    # get active players including eliminated players
    def get_active_players(self) -> List[Player]:
        active_players = []
        for player in self.get_turn_order():
            if player.get_active():
                active_players.append(player)
        return active_players

    # gets list of players that were originally active but not eliminated
    def get_active_not_eliminated_players(self) -> List[Player]:

        activate_players = []
        for player in self.get_turn_order():
            if not player.is_eliminated() and player.get_active():
                activate_players.append(player)

        return activate_players

    def get_player_count(self) -> int:
        return len(self.get_active_not_eliminated_players())

    def get_size(self) -> int:
        return self._size

    def in_turn_order(self, player_id: int) -> bool:
        pass

    def get_player(self, player_id: int) -> Player | None:
        ret_player = None
        for player in self:
            if ret_player.get_playerID() == player_id:
                ret_player = player
        return ret_player

    def __iter__(self) -> Iterator[Player] | None:
        if not self._head:
            return None

        current = self._current
        first_iteration = True

        while None is not current and (first_iteration or current != self._current):
            yield current.player  # Yield the player at the current node
            current = current.next
            first_iteration = False  # After the first iteration, we set this to False

    def make_player_head(self) -> bool:
        """resets the current player turn to head"""
        is_success = False
        if self._head:
            self._current = self._head
            is_success = True
        return is_success

    def reset_player_turn(self) -> bool:
        is_success = False
        if self._current != None:
            self._current.player.get_player_turn().reset()
            is_success = True
        return is_success

    def update_suggested_player(self, aCharacter: str, aSpace: "Space"):
        if None is aSpace:
            raise ValueError("Missing valid object")
        turn_order = self.get_turn_order()
        for player in turn_order:
            if player.get_character() == aCharacter:
                player.set_current_location(aSpace)
                player.get_player_turn().set_hasEnteredRoom()
                break

    def get_player_object(self, aCharacter: str):
        playerObj: Player = None
        turn_order = self.get_turn_order(True)
        for player in turn_order:
            if player.get_character() == aCharacter:
                playerObj = player
                break
        return playerObj
