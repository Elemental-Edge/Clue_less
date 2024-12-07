import pytest
from unittest.mock import MagicMock
from Backend.GameManagement.playerGroupings.player_turn import Player_Turn

@pytest.fixture
def setup_player_turn():
    playerturn = Player_Turn()
    return playerturn

def test_initialization(setup_player_turn):
    assert not setup_player_turn.get_hasMadeAccusation()
    assert not setup_player_turn.get_hasMadeSuggestion()
    assert not setup_player_turn.get_hasMoved()
    assert not setup_player_turn.get_hasEnteredRoom()

def test_reset(setup_player_turn):
    setup_player_turn.set_hasEnteredRoom()
    setup_player_turn.set_hasMadeAccusation()
    assert setup_player_turn.get_hasMadeAccusation()
    assert setup_player_turn.get_hasEnteredRoom()
    setup_player_turn.reset()
    assert not setup_player_turn.get_hasMadeAccusation()
    assert not setup_player_turn.get_hasMadeSuggestion()
    assert not setup_player_turn.get_hasMoved()
    assert not setup_player_turn.get_hasEnteredRoom()

def test_setters(setup_player_turn):
    setup_player_turn.set_hasMadeAccusation(True)
    assert setup_player_turn.get_hasMadeAccusation() == True

    setup_player_turn.set_hasMadeSuggestion(True)
    assert setup_player_turn.get_hasMadeSuggestion() == True

    setup_player_turn.set_hasMoved(True)
    assert setup_player_turn.get_hasMoved() == True

    setup_player_turn.set_hasEnteredRoom(True)
    assert setup_player_turn.get_hasEnteredRoom() == True

def test_get_valid_actions_no_actions(setup_player_turn):
    actions = setup_player_turn.get_valid_actions()
    assert actions == ["Accusation", "Move"]  # No suggestions since hasn't entered a room

def test_get_valid_actions_with_room_entered(setup_player_turn):
    setup_player_turn.set_hasEnteredRoom(True)
    actions = setup_player_turn.get_valid_actions()
    assert actions == ["Suggestion", "Accusation", "Move"]

def test_get_valid_actions_with_suggestion_made(setup_player_turn):
    setup_player_turn.set_hasEnteredRoom(True)
    setup_player_turn.set_hasMadeSuggestion(True)
    actions = setup_player_turn.get_valid_actions()
    assert actions == ["Accusation", "Move"]  # Suggestion already made

def test_get_valid_actions_with_accusation_made(setup_player_turn):
    setup_player_turn.set_hasMadeAccusation(True)
    actions = setup_player_turn.get_valid_actions()
    assert actions == []  # Accusation already made

def test_get_valid_actions_with_movement(setup_player_turn):
    setup_player_turn.set_hasMoved(True)
    actions = setup_player_turn.get_valid_actions()
    assert actions == ["Suggestion", "Accusation"]  # Cannot move again