from __future__ import annotations
from Backend.cardGroupings.Card import Card, CardType
from random import shuffle

class Deck():
    """
    Deck: Representative a collection of Cards

    This class provides methods for the management of a deck of cards. It provides
    operations for shuffling, dealing, adding, and removing cards.

    Attributes:
        cards (List: Card): List of Cards in the deck
    """
    def __init__(self):
        # Initialize Deck with an empty list of cards
        self._cards = []

    def add_card(self, card: Card):
        if card in self.cards:
            raise ValueError(f"The card '{card._name}' is already in the deck.")
        self.cards.append(card)

    def __contains__(self, card):
        return card in self._cards

    def shuffle(self):
        """Shuffle the deck of cards."""
        shuffle(self._cards)

    def deal(self) -> Card:
        """Deal a card from the deck. Returns None if the deck is empty."""
        if self._cards:
            return self._cards.pop()
        return None

    def is_empty(self) -> bool:
        return len(self._cards) == 0

    def add_card(self, card: Card):
        """Add a card to the deck."""
        if isinstance(card, Card):
            if card in self._cards:
                raise ValueError(f"The card '{card._name}' is already in the deck.")
            self._cards.append(card)
        else:
            raise ValueError("Must add an instance of Card.")

    def remove_card(self, card: Card):
        """Remove a card from the deck."""
        if card in self._cards:
            self._cards.remove(card)
        else:
            raise ValueError("Card not found in the deck.")

    def get_deck(self) -> list:
        """Return the current state of the deck."""
        return self._cards

# Sample
if __name__ == "__main__":
    deck = Deck()

    # Create some cards
    card1 = Card(Card.VALID_SUSPECTS[2], CardType.SUSPECT)
    card2 = Card(Card.VALID_ROOMS[4], CardType.ROOM)
    card3 = Card(Card.VALID_WEAPONS[1], CardType.WEAPON)
    card4 = Card(Card.VALID_WEAPONS[4], CardType.WEAPON)

    # Add cards to the deck
    deck.add_card(card1)
    deck.add_card(card2)
    deck.add_card(card3)
    deck.add_card(card4)

    # Display the deck
    print("Deck before shuffling:", deck.get_deck())

    # Shuffle the deck
    deck.shuffle()
    print("Deck after shuffling:", deck.get_deck())

    # Remove a card
    deck.remove_card(card2)
    print("Deck after removing a card:", deck.get_deck())

    # Deal a card
    dealt_card = deck.deal()
    print("Dealt card:", dealt_card)

    # Display the deck after dealing
    print("Deck after dealing a card:", deck.get_deck())

