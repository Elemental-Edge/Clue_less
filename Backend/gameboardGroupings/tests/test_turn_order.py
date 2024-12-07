from __future__ import annotations
import pytest
from unittest.mock import MagicMock
from Backend.GameManagement.playerGroupings.player import Player
from Backend.gameboardGroupings.turn_order import TurnOrder
from Backend.cardGroupings.Card import Card

@pytest.fixture
def setup_turn_order():
    """Fixture to set up a TurnOrder instance with mock players."""
    turn_order = TurnOrder()

    # Create mock players
    player1 = MagicMock(spec=Player)
    player1.playerName = "Player 1"
    player1.character = Card.VALID_SUSPECTS[3]
    player1.get_character = MagicMock(return_value=Card.VALID_SUSPECTS[3])

    player2 = MagicMock(spec=Player)
    player2.playerName = "Player 2"
    player2.character = Card.VALID_SUSPECTS[2]
    player2.get_character = MagicMock(return_value=Card.VALID_SUSPECTS[2])

    player3 = MagicMock(spec=Player)
    player3.playerName = "Player 3"
    player3.character = Card.VALID_SUSPECTS[1]
    player3.get_character = MagicMock(return_value=Card.VALID_SUSPECTS[1])

    # Add players to the turn order
    turn_order.add_player(player1)
    turn_order.add_player(player2)
    turn_order.add_player(player3)

    return turn_order, [player1, player2, player3]

def test_turn_order_iteration(setup_turn_order):
    turn_order, players = setup_turn_order

    # Iterate through the turn order and collect results
    iterated_players = [player for player in turn_order]

    i: int =3
    for player in turn_order:
        assert player.get_character() == Card.VALID_SUSPECTS[i]
        i-=1


    # Check if the iterated players match the original players in the correct order
    assert iterated_players == players
    assert 3 == len(iterated_players)
    assert len(iterated_players) == len(players)
