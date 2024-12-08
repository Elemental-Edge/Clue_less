import pytest
from Backend.cardGroupings.Card import Card, CardType
from Backend.cardGroupings.Hand import Hand
from Backend.GameManagement.playerGroupings.player import (
    Player,
)
from Backend.gameboardGroupings.space import Hallway, Room, CornerRoom
from Backend.commons import ValidSuspect


@pytest.fixture
def setup_player():
    player = Player("Aron", 1234)
    return player


def test_initialization(setup_player):
    assert setup_player.get_player_name() == "Aron"
    assert setup_player.get_playerID() == 1234
    assert not setup_player.is_eliminated()


def test_receive_card_dealt(setup_player):
    card = Card(ValidSuspect.PLUM, CardType.SUSPECT)
    setup_player.receive_card_dealt(card)
    # Check that the card has been added
    assert len(setup_player.get_hand().get_hand()) == 1


def test_get_valid_moves_empty_hallway(setup_player):
    # Set the current location to an empty hallway
    Hallway1 = Hallway("Hallway1")
    Hallway2 = Hallway("Hallway2")
    Hallway1.add_adjacent_space(Hallway2)
    setup_player.set_current_location(Hallway1)
    valid_moves = setup_player.get_valid_moves()
    assert len(valid_moves) == 1  # Should return the adjacent hallway space


def test_get_valid_moves_non_empty_hallway(setup_player):
    Hallway1 = Hallway("Hallway1")
    Hallway2 = Hallway("Hallway2")
    Hallway2.add_player_count()
    Hallway1.add_adjacent_space(Hallway2)
    setup_player.set_current_location(Hallway1)
    valid_moves = setup_player.get_valid_moves()
    assert len(valid_moves) == 0  # Should not return the non-empty space


def test_get_valid_moves_room(setup_player):
    Hallway1 = Hallway("Hallway1")
    Hallway2 = Hallway("Hallway2")
    Room1 = Room("Room1")
    Room2 = CornerRoom("Room2")
    Hallway1.add_adjacent_space(Hallway2)
    Hallway1.add_adjacent_space(Room1)
    Hallway1.add_adjacent_space(Room2)
    setup_player.set_current_location(Hallway1)
    valid_moves = setup_player.get_valid_moves()
    assert (
        len(valid_moves) == 3
    )  # Should return both adjacent spaces including the room


def test_get_hand(setup_player):
    assert isinstance(
        setup_player.get_hand(), Hand
    )  # Ensure it returns an instance of Hand


def test_set_current_location(setup_player):
    Hallway1 = Hallway("Hallway1")
    setup_player.set_current_location(Hallway1)
    assert setup_player.get_current_location() == Hallway1
