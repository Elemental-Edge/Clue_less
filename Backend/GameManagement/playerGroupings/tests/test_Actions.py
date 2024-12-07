from __future__ import annotations
import pytest
from unittest.mock import MagicMock, patch
from Backend.gameboardGroupings.turn_order import TurnOrder
from Backend.GameManagement.playerGroupings.player import Player
from unittest.mock import MagicMock, patch
from Backend.gameboardGroupings.turn_order import TurnOrder
from Backend.GameManagement.playerGroupings.player import Player
from Backend.GameManagement.playerGroupings.Actions import Accusation, Suggestion, Move
from Backend.cardGroupings.Card import Card, CardType
from Backend.cardGroupings.Hand import Hand
from Backend.gameboardGroupings.space import Hallway, SpaceType, Space, Room
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
    result = setup_accusation.makeAccusation(Card.VALID_SUSPECTS[3],
                                            Card.VALID_WEAPONS[3],Card.VALID_ROOMS[3])
    assert result is True
    assert setup_accusation.get_player().get_player_turn().get_hasMadeAccusation() is True
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
    player1.get_hand().add_card(Card(Card.VALID_ROOMS[3], card_type=CardType.ROOM))
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
    suggestion, player1, player2, player3, player4  = setup_suggestion

    # Set up test cards without any disproving cards
    suspect_card = Card(Card.VALID_SUSPECTS[0], card_type=CardType.SUSPECT)
    weapon_card = Card(Card.VALID_WEAPONS[2], card_type=CardType.WEAPON)
    room_card = Card(Card.VALID_ROOMS[4], card_type=CardType.ROOM)

    # Player2 has no cards to disprove the suggestion
    player2.get_hand()

    # Create the suggestion
    player1.get_hand().add_card(suspect_card)
    player1.get_hand().add_card(weapon_card)
    player1.get_hand().add_card(room_card)

    # Execute the suggestion
    next_player, disproved_cards = suggestion.makeSuggestion(Card.VALID_SUSPECTS[0], Card.VALID_WEAPONS[0], Card.VALID_ROOMS[0])

    # Check the results
    assert next_player == None
    assert disproved_cards == []

def test_makeSuggestion_bad_inputs(setup_suggestion):
    # Create a Suggestion instance
    name = "Jamar"
    suggestion = Suggestion(None)
    with pytest.raises(ValueError, match="Turn Order Object is None: No Players in Turn Order"):
        suggestion.makeSuggestion(Card.VALID_SUSPECTS[0], Card.VALID_WEAPONS[0], Card.VALID_ROOMS[0])
    suggestion = setup_suggestion[0]
    with pytest.raises(ValueError, match=f"{name} is not a valid suspect."):
        suggestion.makeSuggestion(name, Card.VALID_WEAPONS[0], Card.VALID_ROOMS[0])
    with pytest.raises(ValueError, match=f"{Card.VALID_WEAPONS[0]} is not a valid suspect."):
        suggestion.makeSuggestion(Card.VALID_WEAPONS[0], Card.VALID_SUSPECTS[0], Card.VALID_ROOMS[0])

@pytest.fixture
def setup_move():
    # Create a mock player and turn order for testing
    room_kitchen = Room("Kitchen")
    room_Living = Room("Living")
    hallway1 = Hallway("Hallway1")
    hallway1.add_adjacent_space(room_Living)
    hallway1.add_adjacent_space(room_kitchen)

    player1 = Player("Jon")
    player1.set_current_location(room_kitchen)
    player2 = Player("Jamar")
    player2.set_current_location(room_Living)
    player3 = Player("Aron")
    player4 = Player("Jamie")
    turn_order = TurnOrder()
    turn_order.add_player(player1)
    turn_order.add_player(player2)
    turn_order.add_player(player3)
    turn_order.add_player(player4)

    move_action = Move(turn_order)
    return move_action, room_kitchen, room_Living, hallway1

def test_makeMove_invalid_destination(setup_move):
    move_action = setup_move[0]
    with pytest.raises(ValueError, match=f"Empty Destination Object Case File"):
        result = move_action.makeMove(None)

def test_makeMove_hallway(setup_move):
    move_action, kitchen, living, Hallway= setup_move
    result = move_action.makeMove(Hallway)
    assert result is True

def test_makeMove_not_adjacent(setup_move):
    move_action = setup_move[0]
    mock_space = Room("Bathroom")
    move_action.makeMove(mock_space)
    assert mock_space not in move_action.get_player().get_current_location().get_adjacent_spaces()
