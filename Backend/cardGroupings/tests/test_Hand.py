import pytest
from Backend.cardGroupings.Card import Card, CardType
from Backend.cardGroupings.Hand import Hand

@pytest.fixture
def card_suspect():
    """Fixture to create a Suspect Card instance for testing."""
    return Card(Card.VALID_SUSPECTS[2], CardType.SUSPECT)

@pytest.fixture
def card_weapon():
    """Fixture to create a Weapon Card instance for testing."""
    return Card(Card.VALID_WEAPONS[1], CardType.WEAPON)

@pytest.fixture
def card_room():
    """Fixture to create a Room Card instance for testing."""
    return Card(Card.VALID_ROOMS[4], CardType.ROOM)

def test_initial_deck_is_empty():
    hand = Hand()
    assert len(hand.get_hand()) == 0

def test_add_card_to_deck(card_weapon):
    hand = Hand()
    hand.add_card(card_weapon)
    assert len(hand.get_hand()) == 1
    assert hand.get_hand()[0] == card_weapon

def test_remove_card_from_deck(card_suspect):
    hand = Hand()
    hand.add_card(card_suspect)
    hand.remove_card(card_suspect)
    assert len(hand.get_hand()) == 0

def test_remove_nonexistent_card(card_suspect, card_room):
    hand = Hand()
    hand.add_card(card_suspect)
    with pytest.raises(ValueError, match="Card not found in the hand."):
        hand.remove_card(card_room)  # Attempt to remove a card that isn't in the hand

def test_clear_hand(card_suspect, card_weapon, card_room):
    hand = Hand()
    hand.add_card(card_suspect)
    hand.add_card(card_weapon)
    hand.add_card(card_room)
    hand.clear_hand()
    assert len(hand.get_hand()) == 0  # Hand should be empty after dealing the only card

def test_add_duplicate_card_to_hand(card_weapon):
    hand = Hand()
    hand.add_card(card_weapon)  # Add the card once
    with pytest.raises(ValueError, match=f"The card '{card_weapon.get_name()}' is already in the hand."):
        hand.add_card(card_weapon)  # Attempt to add the same card again