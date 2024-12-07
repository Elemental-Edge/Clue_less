import pytest
from unittest.mock import MagicMock
from Backend.cardGroupings.Card import Card, CardType
from Backend.cardGroupings.Hand import Hand
from Backend.GameManagement.playerGroupings.player import Player  # Replace 'your_module' with the actual module name
from Backend.gameboardGroupings.space import Hallway
@pytest.fixture
def player():
    player = Player("Aron")
    player.playerHand = Hand()  # Assign a mock hand to the player
    return player

def test_initialization(player):
    assert player.get_player_name() == "Aron"
    assert not player.is_eliminated()

def test_receive_card_dealt(player):
    card = Card(Card.VALID_SUSPECTS[4], CardType.SUSPECT)  # Assuming Card has a default constructor
    player.receive_card_dealt(card)
    assert len(player.get_hand().get_hand()) == 1  # Check that the card has been added
"""
def test_get_valid_moves_empty_hallway(player):
    player.set_current_location(Hallway("Kitchen")) # Set the current location to an empty hallway
    valid_moves = player.get_valid_moves()
    assert len(valid_moves) == 1  # Should return the adjacent hallway space

def test_get_valid_moves_non_empty_hallway(player):
    player.currLocation = MockSpace('HALLWAY', is_empty=False)  # Set to a non-empty hallway
    valid_moves = player.get_valid_moves()
    assert len(valid_moves) == 0  # Should not return the non-empty space

def test_get_valid_moves_room(player):
    player.currLocation = MockSpace('ROOM', is_empty=True)  # Set to a room
    valid_moves = player.get_valid_moves()
    assert len(valid_moves) == 2  # Should return both adjacent spaces including the room

def test_get_hand(player):
    assert isinstance(player.get_hand(), Hand)  # Ensure it returns an instance of Hand

def test_set_current_location(player):
    new_space = MockSpace('HALLWAY')
    player.set_current_location(new_space)
    assert player.get_current_location() == new_space

def test_get_character(player):
    player.character = "Detective"
    assert player.get_character() == "Detective"

def test_str_method(player):
    player.character = "Detective"
    assert str(player) == "Detective"
    """