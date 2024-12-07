# tests/test_card.py
import pytest
from Backend.cardGroupings.Card import CardType, Card

@pytest.fixture
def card():
    """Fixture to create a Card instance for testing."""
    return Card(Card.VALID_SUSPECTS[2], CardType.SUSPECT)

def test_invalid_suspect_name():
    with pytest.raises(ValueError, match="King Jamar is not a valid suspect."):
        Card("King Jamar", CardType.SUSPECT)

def test_invalid_weapon_name():
    with pytest.raises(ValueError, match="Club Dallas is not a valid weapon."):
        Card("Club Dallas", CardType.WEAPON)

def test_valid_suspect_name():
    Card("scarlet", CardType.SUSPECT)  # Should not raise an exception

def test_valid_room_name():
    Card(Card.VALID_ROOMS[0], CardType.ROOM)  # Should not raise an exception

def test_card_initialization(card):
    """Test the initialization of the Card class."""
    assert card.get_name() == Card.VALID_SUSPECTS[2]
    assert card.get_card_type() == CardType.SUSPECT

def test_card_equality():
    """Test the equality operator."""
    card1 = Card(Card.VALID_WEAPONS[3], CardType.WEAPON)
    card2 = Card(Card.VALID_WEAPONS[3], CardType.WEAPON)
    card3 = Card(Card.VALID_WEAPONS[1], CardType.WEAPON)

    assert card1 == card2  # Same name and type
    assert card1 != card3  # Different name

def test_card_repr(card):
    """Test the __repr__ method."""
    assert repr(card) == f"Card(name='{Card.VALID_SUSPECTS[2]}', card_type=CardType.SUSPECT)"

def test_card_str(card):
    """Test the __str__ method."""
    assert str(card) == f"name='{Card.VALID_SUSPECTS[2]}'"