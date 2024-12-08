from __future__ import annotations
import pytest
from Backend.GameManagement.playerGroupings.player import Player
from Backend.gameboardGroupings.turn_order import TurnOrder
from Backend.cardGroupings.Card import Card
from Backend.commons import ValidWeapons, ValidRooms, ValidSuspect

@pytest.fixture
def setup_turn_order():
    """Fixture to set up a TurnOrder instance with mock players."""
    turn_order = TurnOrder()

    # Create mock players
    player1 = Player("Jamar", 1)
    player1.set_character(ValidSuspect.WHITE)

    player2 = Player("Aron", 2)
    player2.set_character(ValidSuspect.SCARLET)

    player3 = Player("Jon", 3)
    player3.set_character(ValidSuspect.PLUM)

    player4 = Player("Jamie", 3)
    player4.set_character(ValidSuspect.PEACOCK)

    player5 = Player("Ace", 3)
    player5.set_character(ValidSuspect.MUSTARD)

    # Add players to the turn order
    turn_order.add_player(player1)
    turn_order.add_player(player2)
    turn_order.add_player(player3)
    turn_order.add_player(player4)
    turn_order.add_player(player5)

    return turn_order, turn_order.get_turn_order()


def test_add_first_player_creates_circular_list():
    # Arrange
    turn_order = TurnOrder()

    assert turn_order._head is None
    assert turn_order._tail is None
    assert turn_order._current is None
    player = Player("Jamar", 1)

    # Act
    turn_order.add_player(player)

    # Assert
    assert turn_order._head is not None
    assert turn_order._tail is not None
    assert turn_order._current is not None
    assert turn_order._head.next == turn_order._head
    assert turn_order._tail.next == turn_order._head
    assert turn_order.get_player_count() == 1


def test_adding_multiple_players(setup_turn_order):
    turn_order, players = setup_turn_order
    assert turn_order._head is not None
    assert turn_order._tail is not None
    assert turn_order._current is not None
    assert turn_order._head.next.player == players[1]
    assert turn_order._head.next.next.player == players[2]
    assert turn_order._head.next.next.next.next.next == turn_order._head
    assert turn_order._tail.next == turn_order._head
    assert turn_order.get_player_count() == 5


def test_advance_turn_moves_to_next_player(setup_turn_order):
    turn_order, players = setup_turn_order

    # Act & Assert
    assert turn_order.get_current_turn() == players[0]
    turn_order.advance_turn()
    assert turn_order.get_current_turn() == players[1]
    turn_order.advance_turn()
    assert turn_order.get_current_turn() == players[2]
    turn_order.advance_turn()
    assert turn_order.get_current_turn() == players[3]
    turn_order.advance_turn()
    assert turn_order.get_current_turn() == players[4]
    turn_order.advance_turn()
    assert turn_order.get_current_turn() == players[0]


# Removing a player maintains circular list structure
def test_remove_middle_player_maintains_circular_structure(setup_turn_order):
    turn_order, players = setup_turn_order
    # Act
    removed_player = turn_order.remove_player(players[3])

    # Assert
    assert removed_player == players[3]
    assert turn_order.get_player_count() == 4
    assert turn_order._head.player == players[0]
    assert turn_order._tail.player == players[4]
    assert turn_order._head.next.next.next == turn_order._tail
    assert turn_order._tail.next == turn_order._head


# Removing first player maintains circular list structure
def test_remove_head_player_maintains_circular_structure(setup_turn_order):
    turn_order, players = setup_turn_order
    # Act
    removed_player = turn_order.remove_player(players[0])

    # Assert
    assert removed_player == players[0]
    assert turn_order.get_player_count() == 4
    assert turn_order._head.player == players[1]
    assert turn_order._tail.player == players[4]
    assert turn_order._head.next.next.next == turn_order._tail
    assert turn_order._tail.next == turn_order._head


# Removing a player maintains circular list structure
def test_remove_tail_player_maintains_circular_structure(setup_turn_order):
    turn_order, players = setup_turn_order
    # Act
    removed_player = turn_order.remove_player(players[4])

    # Assert
    assert removed_player == players[4]
    assert turn_order.get_player_count() == 4
    assert turn_order._head.player == players[0]
    assert turn_order._tail.player == players[3]
    assert turn_order._head.next.next.next == turn_order._tail
    assert turn_order._tail.next == turn_order._head


# Getting turn order returns list of players in correct sequence
def test_get_turn_order_returns_correct_sequence():
    # Arrange
    turn_order = TurnOrder()
    player1 = Player("Player1", 1)
    player2 = Player("Player2", 2)
    player3 = Player("Player3", 3)

    # Act
    turn_order.add_player(player1)
    turn_order.add_player(player2)
    turn_order.add_player(player3)
    result = turn_order.get_turn_order()

    # Assert
    assert result == [player1, player2, player3]

    # Randomizing order maintains all players but in different sequence


def test_randomize_order_changes_sequence(setup_turn_order):
    turn_order, players = setup_turn_order

    original_order = turn_order.get_turn_order()

    # Act
    turn_order.randomize_order()

    randomized_order = turn_order.get_turn_order()

    # Assert
    for item in original_order:
        assert (item in randomized_order)
    # Ensure all players are still present
    assert original_order != randomized_order  # Ensure the order has changed


def test_turn_order_iteration(setup_turn_order):
    turn_order, players = setup_turn_order

    # Iterate through the turn order and collect results
    iterated_players = [player for player in turn_order]

    ValidSuspectList = [ValidSuspect.WHITE,
                        ValidSuspect.SCARLET,
                        ValidSuspect.PLUM,
                        ValidSuspect.PEACOCK,
                        ValidSuspect.MUSTARD]
    i: int = 0
    for player in turn_order:
        assert player.get_character() == ValidSuspectList[i]
        i += 1

    # Check if the iterated players match the original players in the correct order
    assert iterated_players == players
    assert 5 == len(iterated_players)
    assert len(iterated_players) == len(players)
