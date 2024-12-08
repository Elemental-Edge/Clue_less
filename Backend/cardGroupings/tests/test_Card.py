# tests/test_card.py
import pytest
from Backend.cardGroupings.Card import CardType, Card
from Backend.commons import ValidRooms, ValidSuspect, ValidWeapons


@pytest.fixture
def card():
    """Fixture to create a Card instance for testing."""
    return Card(ValidSuspect.GREEN, CardType.SUSPECT)


def test_invalid_suspect_name():
    with pytest.raises(ValueError, match="King Jamar is not a valid suspect."):
        Card("King Jamar", CardType.SUSPECT)


def test_invalid_weapon_name():
    with pytest.raises(ValueError, match="Club Dallas is not a valid weapon."):
        Card("Club Dallas", CardType.WEAPON)


def test_valid_suspect_name():
    Card(ValidSuspect.PLUM, CardType.SUSPECT)  # Should not raise an exception


def test_valid_room_name():
    Card(ValidRooms.DINING, CardType.ROOM)  # Should not raise an exception


def test_card_initialization(card):
    """Test the initialization of the Card class."""
    assert card.get_name() == ValidSuspect.GREEN
    assert card.get_card_type() == CardType.SUSPECT


def test_card_equality():
    """Test the equality operator."""
    card1 = Card(ValidWeapons.CANDLESTICK, CardType.WEAPON)
    card2 = Card(ValidWeapons.CANDLESTICK, CardType.WEAPON)
    card3 = Card(ValidWeapons.PIPE, CardType.WEAPON)

    assert card1 == card2  # Same name and type
    assert card1 != card3  # Different name


def test_card_repr(card):
    """Test the __repr__ method."""
    assert (
        repr(card) == f"Card(name='{ValidSuspect.GREEN}', card_type=CardType.SUSPECT)"
    )


def test_card_str(card):
    """Test the __str__ method."""
    assert str(card) == f"name='{ValidSuspect.GREEN}'"
