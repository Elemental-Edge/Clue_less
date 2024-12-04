from __future__ import annotations
import pytest
from unittest.mock import MagicMock
from Backend.GameManagement.playerGroupings.Actions import Accusation, Suggestion, Move
from Backend.cardGroupings.Card import Card
@pytest.fixture
def setup_accusation():
    case_file = MagicMock()
    case_file.has_card.side_effect = lambda card: card._name in [Card.VALID_SUSPECTS[3], Card.VALID_WEAPONS[3], Card.VALID_ROOMS[3]]
    accusation = Accusation(case_file)
    return accusation

def test_makeAccusation_correct(setup_accusation):
    result = setup_accusation.makeAccusation(Card.VALID_SUSPECTS[3], Card.VALID_WEAPONS[3], Card.VALID_ROOMS[3])
    assert result is True

def test_makeAccusation_incorrect(setup_accusation):
    result = setup_accusation.makeAccusation(Card.VALID_SUSPECTS[1], Card.VALID_WEAPONS[3], Card.VALID_ROOMS[3])
    assert result is False

def test_makeAccusation_badInputs(setup_accusation):
    result = setup_accusation.case_file.display_hand()
    assert result is True

"""

@pytest.fixture
def setup_suggestion():
    player = MagicMock(spec=Player)
    turn_order = [MagicMock(spec=Player), MagicMock(spec=Player)]
    suggestion = Suggestion(player, turn_order)
    return suggestion, player, turn_order

def test_makeSuggestion_no_disprove(setup_suggestion):
    suggestion, player, turn_order = setup_suggestion
    turn_order[0].isEliminated = False
    turn_order[0].playerHand.hand = MagicMock()
    turn_order[0].playerHand.hand.has_card.return_value = False

    player.playerHand = MagicMock()
    player.playerHand.hand = MagicMock()

    result = suggestion.makeSuggestion('Suspect1', 'Weapon1', 'Room1')
    assert isinstance(result, tuple)
    assert result[0] is None  # No player to disprove
    assert result[1].isEmpty()  # No disprove cards

def test_makeSuggestion_with_disprove(setup_suggestion):
    suggestion, player, turn_order = setup_suggestion
    turn_order[0].isEliminated = False
    turn_order[0].playerHand.hand = MagicMock()
    turn_order[0].playerHand.hand.has_card.return_value = True

    player.playerHand = MagicMock()
    player.playerHand.hand = MagicMock()

    result = suggestion.makeSuggestion('Suspect1', 'Weapon1', 'Room1')
    assert isinstance(result, tuple)
    assert result[0] is not None  # There should be a player to disprove
    assert not result[1].isEmpty()  # There should be disprove cards


@pytest.fixture
def setup_move():
    player = MagicMock(spec=Player)
    player.currLocation = MagicMock()
    player.prevLocation = None
    player.currLocation.get_adjacent_spaces.return_value = []

    move_action = Move(player, MagicMock())
    return move_action, player

def test_makeMove_invalid_destination(setup_move):
    move_action, _ = setup_move
    result = move_action.makeMove(None)
    assert result is False

def test_makeMove_hallway(setup_move):
    move_action, _ = setup_move
    mock_space = MagicMock()
    mock_space.get_space_type.return_value = SpaceType.HALLWAY
    result = move_action.makeMove(mock_space)
    assert result is False

def test_makeMove_not_adjacent(setup_move):
    move_action, player = setup_move
    mock_space = MagicMock()
    mock_space.get_space_type.return_value = SpaceType.ROOM
    move_action.makeMove(mock_space)
    assert mock_space not in player.currLocation.get_adjacent_spaces()

def test_makeMove_success(setup_move):
    move_action, player = setup_move
    mock_space = MagicMock()
    mock_space.get_space_type.return_value = SpaceType.ROOM
    player.currLocation.get_adjacent_spaces.return_value = [mock_space]

    result = move_action.makeMove(mock_space)
    assert result is True
    assert player.currLocation == mock_space

"""