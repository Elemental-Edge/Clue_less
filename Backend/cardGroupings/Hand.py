from __future__ import annotations
from Backend.cardGroupings.Card import Card, CardType


class Hand:
    """
    Hand: Representative a collection of Cards

    This class provides methods for the management of a hand of cards.
    It provides operations for shuffling, dealing, adding,
    and removing cards.

    Attributes:
        cards (List: Card): List of Cards in the hand
    """

    def __init__(self):
        # Initialize Hand with an empty list of cards
        self._cards = []

    def add_card(self, card: Card):
        """Add a card to the hand."""
        if isinstance(card, Card):
            if card in self._cards:
                raise ValueError(f"The card '{card._name}' is already in the hand.")
            self._cards.append(card)
        else:
            raise ValueError("Must add an instance of Card.")

    def remove_card(self, card: Card):
        """Remove a card from the hand."""
        if card in self._cards:
            self._cards.remove(card)
        else:
            raise ValueError("Card not found in the hand.")

    def get_hand(self) -> list:
        """Return the current state of the hand."""
        return self._cards

    def clear_hand(self):
        """Clear all cards from the hand."""
        self._cards.clear()

    def has_card(self, card: Card):
        """Check if a specific card is in hand."""
        return card in self._cards

    def sort_hand(self):
        """Sort the cards in hand."""
        self._cards.sort()

    def display_hand(self):
        """Display the cards in hand."""
        return ", ".join(str(card) for card in self._cards)

    def isEmpty(self):
        "Returns true if the list is empty"
        return 0 == len(self._cards)

    def __str__(self):
        toReturn = []
        for card in self._cards:
            toReturn.append(str(card) + " ")
        return toReturn


# Sample
if __name__ == "__main__":
    hand = Hand()

    # Create some cards
    card1 = Card(Card.VALID_SUSPECTS[2], CardType.SUSPECT)
    card2 = Card(Card.VALID_ROOMS[4], CardType.ROOM)
    card3 = Card(Card.VALID_WEAPONS[1], CardType.WEAPON)

    # Add cards to the hand
    hand.add_card(card1)
    hand.add_card(card2)
    hand.add_card(card3)

    # Display the hand after dealing
    print("Hand after dealing a card:", hand.get_hand())

    # Remove a card
    hand.remove_card(card2)
    print("Hand after removing a card:", hand.get_hand())
