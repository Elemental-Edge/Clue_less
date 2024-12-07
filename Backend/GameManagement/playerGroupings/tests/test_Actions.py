from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch
from Backend.gameboardGroupings.turn_order import TurnOrder
from Backend.GameManagement.playerGroupings.player import Player
from Backend.GameManagement.playerGroupings.Actions import Accusation, Suggestion, Move
from Backend.cardGroupings.Card import Card, CardType
from Backend.cardGroupings.Hand import Hand
from Backend.gameboardGroupings.space import Hallway, SpaceType, Space
@pytest.fixture
def setup_accusation():
    case_file = MagicMock(spec=Hand)
    case_file.has_card.side_effect = lambda card: card._name in [Card.VALID_SUSPECTS[3],
                                                                 Card.VALID_WEAPONS[3],
                                                                 Card.VALID_ROOMS[3]]
        # Create a mock player and turn order for testing
    player1 = Player("Jon")
    player2 = Player("Jamar")
    player3 = Player("Aron")
    player4 = Player("Jamie")
    turn_order = TurnOrder()
    turn_order.add_player(player1)
    turn_order.add_player(player2)
    turn_order.add_player(player3)
    turn_order.add_player(player4)
    accusation = Accusation(turn_order, case_file)
    return accusation

def test_makeAccusation_correct(setup_accusation):
    result = setup_accusation.makeAccusation(Card.VALID_SUSPECTS[3],
                                            Card.VALID_WEAPONS[3],Card.VALID_ROOMS[3])
    assert result is True
    assert setup_accusation.get_player().get_player_turn().get_hasMadeAccusation() is True

def test_makeAccusation_incorrect(setup_accusation):
    result = setup_accusation.makeAccusation(Card.VALID_SUSPECTS[1], Card.VALID_WEAPONS[3], Card.VALID_ROOMS[3])
    assert result is False

def test_makeAccusation_bad_inputs(setup_accusation):
    # Create a Suggestion instance
    name = "Jamar"
    accusation = Accusation(TurnOrder(), None)
    with pytest.raises(ValueError, match="Case File Object is NULL"):
        accusation.makeAccusation(Card.VALID_SUSPECTS[0], Card.VALID_WEAPONS[0], Card.VALID_ROOMS[0])
    accusation = Accusation(None, Hand())
    with pytest.raises(ValueError, match=f"Turn Order Object is None: No Players in Turn Order"):
        accusation.makeAccusation(name, Card.VALID_WEAPONS[0], Card.VALID_ROOMS[0])
    with pytest.raises(ValueError, match=f"{name} is not a valid suspect."):
        setup_accusation.makeAccusation(name, Card.VALID_WEAPONS[0], Card.VALID_ROOMS[0])
    assert setup_accusation.get_player().get_player_turn().get_hasMadeAccusation() is False
    with pytest.raises(ValueError, match=f"{Card.VALID_WEAPONS[0]} is not a valid suspect."):
        setup_accusation.makeAccusation(Card.VALID_WEAPONS[0], Card.VALID_SUSPECTS[0], Card.VALID_ROOMS[0])
    assert setup_accusation.get_player().get_player_turn().get_hasMadeAccusation() is False

@pytest.fixture
def setup_suggestion():
    from Backend.GameManagement.playerGroupings.player import Player
    from Backend.gameboardGroupings.turn_order import TurnOrder
    from Backend.GameManagement.playerGroupings.player_turn import Player_Turn
    # Create a mock player and turn order for testing
    player1 = Player("Jon")
    player2 = Player("Jamar")
    player3 = Player("Aron")
    player4 = Player("Jamie")
    turn_order = TurnOrder()
    turn_order.add_player(player1)
    turn_order.add_player(player2)
    turn_order.add_player(player3)
    turn_order.add_player(player4)

    # Create a Suggestion instance
    suggestion = Suggestion(turn_order)

    return suggestion, player1, player2, player3, player4

def test_makeSuggestion_disproves(setup_suggestion):
    suggestion, player1, player2, player3, player4 = setup_suggestion

    # Set up test cards
    suspect_card = Card(Card.VALID_SUSPECTS[0], card_type=CardType.SUSPECT)
    weapon_card = Card(Card.VALID_WEAPONS[2], card_type=CardType.WEAPON)
    room_card = Card(Card.VALID_ROOMS[4], card_type=CardType.ROOM)

    # Add cards to player2's hand to disprove the suggestion
    player3.get_hand().add_card(Card(Card.VALID_ROOMS[1], card_type=CardType.ROOM))
    player3.get_hand().add_card(suspect_card)
    player4.get_hand().add_card(Card(Card.VALID_ROOMS[5], card_type=CardType.ROOM))
    player2.get_hand().add_card(Card(Card.VALID_ROOMS[2], card_type=CardType.ROOM))

    # Create the suggestion
    player1.get_hand().add_card(suspect_card)
    player1.get_hand().add_card(weapon_card)
    player1.get_hand().add_card(room_card)

    # Execute the suggestion
    next_player, disproved_cards = suggestion.makeSuggestion(Card.VALID_SUSPECTS[0],
                                                            Card.VALID_WEAPONS[0],
                                                            Card.VALID_ROOMS[0])

    # Check the results
    assert next_player == player3
    assert suggestion.get_player().get_player_turn().get_hasMadeSuggestion() is True
    assert Card.VALID_SUSPECTS[0] in disproved_cards[0]

def test_makeSuggestion_no_disprove(setup_suggestion):
    suggestion, player1, player2, player3 = setup_suggestion

    # Set up test cards without any disproving cards
    suspect_card = Card(Card.VALID_SUSPECTS[0], card_type=CardType.SUSPECT)
    weapon_card = Card(Card.VALID_WEAPONS[2], card_type=CardType.WEAPON)
    room_card = Card(Card.VALID_ROOMS[4], card_type=CardType.ROOM)

    # Player2 has no cards to disprove the suggestion
    player2.get_hand.return_value = Hand()  # Empty hand

    # Create the suggestion
    player1.get_hand.return_value.add_card(suspect_card)
    player1.get_hand.return_value.add_card(weapon_card)
    player1.get_hand.return_value.add_card(room_card)

    # Execute the suggestion
    next_player, disproved_cards = suggestion.makeSuggestion(Card.VALID_SUSPECTS[0], Card.VALID_WEAPONS[0], Card.VALID_ROOMS[0])

    # Check the results
    assert next_player == None
    assert disproved_cards == []

def test_makeSuggestion_bad_inputs(setup_suggestion):
    # Create a Suggestion instance
    name = "Jamar"
    suggestion = Suggestion(Player_Turn(None), None)
    with pytest.raises(ValueError, match="Missing turn order"):
        suggestion.makeSuggestion(Card.VALID_SUSPECTS[0], Card.VALID_WEAPONS[0], Card.VALID_ROOMS[0])
    suggestion = Suggestion(None, TurnOrder())
    with pytest.raises(ValueError, match="Missing Player Turn"):
        suggestion.makeSuggestion(Card.VALID_SUSPECTS[0], Card.VALID_WEAPONS[0], Card.VALID_ROOMS[0])
    suggestion = setup_suggestion[0]
    with pytest.raises(ValueError, match=f"{name} is not a valid suspect."):
        suggestion.makeSuggestion(name, Card.VALID_WEAPONS[0], Card.VALID_ROOMS[0])
    with pytest.raises(ValueError, match=f"{Card.VALID_WEAPONS[0]} is not a valid suspect."):
        suggestion.makeSuggestion(Card.VALID_WEAPONS[0], Card.VALID_SUSPECTS[0], Card.VALID_ROOMS[0])

@pytest.fixture
def setup_move():
        # Create a mock player and turn order for testing
    player1 = MagicMock(spec=Player)
    player1.currLocation = MagicMock()
    player1.prevLocation = None
    player1.currLocation.get_adjacent_spaces.return_value = []
    playerTurn = Player_Turn(player1)
    move_action = Move(playerTurn)
    return move_action, playerTurn

def test_makeMove_invalid_destination(setup_move):
    move_action = setup_move[0]
    with pytest.raises(ValueError, match=f"Empty Destination Object Case File"):
        result = move_action.makeMove(None)

def test_makeMove_hallway(setup_move):
    move_action = setup_move[0]
    mock_space = MagicMock(spec = Hallway)
    mock_space.get_space_type.return_value = SpaceType.HALLWAY
    mock_space.add_player.return_value = True
    result = move_action.makeMove(mock_space)
    assert result is False

def test_makeMove_not_adjacent(setup_move):
    move_action, playerTurn = setup_move
    mock_space = MagicMock(spec=Space)
    mock_space.get_space_type.return_value = SpaceType.ROOM
    move_action.makeMove(mock_space)
    assert mock_space not in playerTurn.get_player().currLocation.get_adjacent_spaces()

def test_makeMove_success(setup_move):
    move_action, playerTurn = setup_move
    mock_space = MagicMock()
    mock_space.get_space_type.return_value = SpaceType.ROOM
    playerTurn.get_player().currLocation.get_adjacent_spaces.return_value = [mock_space]

    result = move_action.makeMove(mock_space)
    assert result is True
    assert playerTurn.get_player().currLocation == mock_space
