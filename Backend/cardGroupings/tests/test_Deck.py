import pytest
from Backend.cardGroupings.Card import Card, CardType
from Backend.cardGroupings.Deck import Deck

@pytest.fixture
def card_suspect():
    """Fixture to create a Suspect Card instance for testing."""
    return Card(Card.VALID_SUSPECTS[2], CardType.SUSPECT)

@pytest.fixture
def card_weapon():
    """Fixture to create a Weapon Card instance for testing."""
    return Card(Card.VALID_WEAPONS[2], CardType.WEAPON)

@pytest.fixture
def card_room():
    """Fixture to create a Room Card instance for testing."""
    return Card(Card.VALID_ROOMS[2], CardType.ROOM)


def test_initial_deck_is_empty():
    deck = Deck()
    assert len(deck.get_deck()) == 0

def test_add_card_to_deck(card_suspect, card_room, card_weapon):
    deck = Deck()
    deck.add_card(card_suspect)
    deck.add_card(card_room)
    deck.add_card(card_weapon)
    assert len(deck.get_deck()) == 3
    assert deck.get_deck()[0] == card_suspect

def test_remove_card_from_deck(card_suspect):
    deck = Deck()
    deck.add_card(card_suspect)
    deck.remove_card(card_suspect)
    assert len(deck.get_deck()) == 0

def test_remove_nonexistent_card(card_suspect, card_room):
    deck = Deck()
    deck.add_card(card_suspect)
    with pytest.raises(ValueError, match="Card not found in the deck."):
        deck.remove_card(card_room)  # Attempt to remove a card that isn't in the deck

def test_shuffle_deck(card_suspect, card_room, card_weapon):
    deck = Deck()
    deck.add_card(card_suspect)
    deck.add_card(card_room)
    deck.add_card(card_weapon)

    original_order = deck.get_deck()
    print(original_order)
    deck.shuffle()
    print(deck.get_deck())
    assert len(deck.get_deck()) == 3
    # Check that the cards are still the same but may be in a different order
    assert deck.get_deck().sort() == original_order.sort()

def test_deal_card(card_suspect):
    deck = Deck()
    deck.add_card(card_suspect)
    dealt_card = deck.deal()
    assert dealt_card == card_suspect
    assert len(deck.get_deck()) == 0  # Deck should be empty after dealing the only card

def test_deal_card_empty_deck():
    deck = Deck()
    assert deck.deal() is None  # Should return None when trying to deal from an empty deck

def test_add_duplicate_card_to_deck(card_suspect):
    deck = Deck()
    deck.add_card(card_suspect)  # Add the card once
    with pytest.raises(ValueError, match=f"The card '{card_suspect.get_name()}' is already in the deck."):
        deck.add_card(card_suspect)  # Attempt to add the same card again