from typing import List
from random import shuffle
from Backend.GameManagement.playerGroupings.player import Player


class Node:
    """A node in the circular singly circular linked list. Stores the 
       reference to Player Object and the next Player in 
       the singly circular linked list"""
    def __init__(self, player: Player):
        self.player = player  # Player this node represents
        self.next = None      # Pointer to the next node


class TurnOrder:
    """Manages the turn order using a circular singly linked list."""
    def __init__(self):
        self.head = None  # First node in the list
        self.tail = None  # Last node in the list
        self.current = None  # Current player's turn

    def add_player(self, player: Player):
        """
        Add a player to the turn order.
        Creates a new node for the player and appends it to the end of the circular list.
        """
        new_node = Node(player)
        if self.head is None:
            # First player in the list
            self.head = new_node
            self.tail = new_node
            new_node.next = new_node  # Circular reference
            self.current = new_node
        else:
            # Append the new node at the end
            self.tail.next = new_node
            new_node.next = self.head
            self.tail = new_node

    def remove_player(self, player: Player) -> None | Player:
        """
        Remove a player from the turn order.
        Traverses the list to find the player and removes their node.
        If the player is the only one, clears the list.
        """
        if self.head:
            prev = self.tail
            current = self.head

        while current != self.tail or prev == self.tail:  # Traverse until full cycle
            if current.player == player:
                if current == self.head and current == self.tail:
                    # Only one player in the list
                    self.head = None
                    self.tail = None
                    self.current = None
                else:
                    # Update links to remove the node
                    prev.next = current.next
                    if current == self.head:
                        self.head = current.next
                    if current == self.tail:
                        self.tail = prev
                    if current == self.current:
                        self.current = current.next
                return current.player  # Return the removed player
            prev = current
            current = current.next
        return None  # Player not found

    def get_current_turn(self) -> Player | None:
        """
        Get the player whose turn it is.
        Returns the player at the `current` node.
        """
        return self.current.player if self.current else None

    def advance_turn(self):
        """
        Move to the next player's turn.
        Updates the `current` pointer to the next node in the list.
        """
        if self.current:
            self.current = self.current.next

    def reverse_order(self):
        """
        Reverse the order of players in the turn order.
        Reverses the direction of the `next` pointers and updates the `head` and `tail`.
        """
        if self.head is None or self.head.next == self.head:
            return  # No players or only one player

        prev = self.tail
        current = self.head
        first_node = self.head

        while current != first_node or prev == self.tail:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node

        # Update head and tail and reconnect the circular link
        self.tail = self.head
        self.head = prev
        self.tail.next = self.head
        self.current = self.head

    def randomize_order(self):
        """
        Randomize the turn order of players.
        Collects all players into a list, shuffles the list, and rebuilds the circular linked list.
        """
        if self.head is None or self.head.next == self.head:
            return  # No players or only one player

        # Collect all players
        players = self.get_turn_order()

        # Shuffle the list of players
        shuffle(players)

        # Rebuild the circular list
        self.head = None
        self.tail = None
        self.current = None
        for player in players:
            self.add_player(player)

    def get_turn_order(self) -> List[Player]:
        """
        Get a list of players in the current turn order.
        Traverses the circular list and collects all players in order.
        """
        players = []
        if self.head is None:
            return players

        current = self.head

        while current != self.tail or len(players) == 0:  # Ensure full cycle
            players.append(current.player)
            current = current.next
        players.append(self.tail.player)  # Add the tail player to the list

        return players
    
    def get_active_players(self) -> List[Player]:
        activate_players = []
        for player in self.get_turn_order():
            if not player.is_eliminated():
                activate_players.append(player)
        return activate_players
