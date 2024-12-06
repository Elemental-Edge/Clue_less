from enum import Enum, auto
from typing import List, Optional, Dict, Set
from Backend.cardGroupings.Deck import Deck
from Backend.cardGroupings.Hand import Hand
from Backend.cardGroupings.Card import Card, CardType
from Backend.GameManagement.playerGroupings.Actions import Accusation, Suggestion, Actions
from Backend.gameboardGroupings.turn_order import TurnOrder
from Backend.GameManagement.playerGroupings.player import Player
from Backend.gameboardGroupings.space import Room, Hallway, Space
from Backend.gameboardGroupings.gameboard import GameBoard
import random

# TODO: Must have odd players to join the game

class GameState(Enum):
    WAITING_FOR_PLAYERS = auto()
    INITIALIZING = auto()
    IN_PROGRESS = auto()
    GAME_OVER = auto()


class GameProcessor:
    """Controls the game flow and manages game state."""

    MIN_PLAYERS = 3
    MAX_PLAYERS = 6
    
    def __init__(self, game_id: str):
        # Game identification
        self.game_id: str = game_id
        
        # Game components
        self.game_board: GameBoard = GameBoard()
        self.main_deck: Deck = Deck()
        self.case_file: Hand = Hand()

        # Game state
        self.state: GameState = GameState.WAITING_FOR_PLAYERS
        self.winner: Player = None

        self.turnOrder: TurnOrder = TurnOrder()
        self._initialize_deck()
    
    def __str__(self):
        return self.state

    def _initialize_deck(self) -> None:
        """Initialize the main deck with all cards."""
        # Add all suspect cards
        for suspect in Card.VALID_SUSPECTS:
            self.main_deck.add_card(Card(suspect, CardType.SUSPECT))

        # Add all weapon cards
        for weapon in Card.VALID_WEAPONS:
            self.main_deck.add_card(Card(weapon, CardType.WEAPON))

        # Add all room cards
        for room in Card.VALID_ROOMS:
            self.main_deck.add_card(Card(room, CardType.ROOM))

    def add_player(self, player_name: str, player_id: int) -> bool:
        """Add a new player to the game."""
        if self.state != GameState.WAITING_FOR_PLAYERS:
            raise ValueError("Cannot add players after game has started")

        if len(self.players) >= self.MAX_PLAYERS:
            raise ValueError("Maximum number of players reached")

        # Create new player
        player = Player(player_name, player_id)
        # TODO: review this function to determine if it can be simplified
        available_characters = set(Card.VALID_SUSPECTS)
        - {p.get_character_name() for p in self.players}
        # {Mustard, Plum} - {Mustard} = {Plum} rand = {Plum}
        player.character = random.choice(list(available_characters))

        # Set starting position
        starting_positions = self.game_board.get_starting_positions()
        player.currLocation = starting_positions[player.character]

        self.turnOrder.add_player(player)

    def start_game(self) -> bool:
        """Initialize and start the game."""
        if len(self.players) < self.MIN_PLAYERS:
            raise ValueError(f"Need at least {self.MIN_PLAYERS} players to start")
        if len(self.players) % self.MIN_PLAYERS != 0:
            raise ValueError(f"{len(self.players)} players, must have a multiple of {self.MIN_PLAYERS} players to start.")

        self.state = GameState.INITIALIZING

        # Create case file
        self._create_case_file()

        # Deal remaining cards
        self._deal_cards()

        self.turnOrder.randomize_order()

        # Start first turn
        self.state = GameState.IN_PROGRESS
        return True

    def _create_case_file(self) -> None:
        """Create the case file by selecting one of each card type."""
        self.main_deck.shuffle()

        # Get one of each type
        suspect = next(card for card in self.main_deck.get_deck()
                      if card.get_card_type() == CardType.SUSPECT)
        weapon = next(card for card in self.main_deck.get_deck()
                     if card.get_card_type() == CardType.WEAPON)
        room = next(card for card in self.main_deck.get_deck()
                   if card.get_card_type() == CardType.ROOM)

        # Remove from main deck and add to case file
        for card in [suspect, weapon, room]:
            self.main_deck.remove_card(card)
            self.case_file.add_card(card)

    def _deal_cards(self) -> None:
        """Deal remaining cards to players."""
        self.main_deck.shuffle()

        # Deal all remaining cards
        for card in self.main_deck.get_deck():
            self.turnOrder.advance_turn()
            current_turn = self.turnOrder.get_current_turn()
            # sets current players turn
            if current_turn:
                current_turn.receive_card_dealt(card)

    def handle_suggestion(self, player: Player, aSuspect: str, aWeapon: str, aRoom: str) -> Optional[tuple[Player, Hand]]:
        """Handle a suggestion from a player."""
        if not self.current_turn or not self.current_turn.isActive:
            raise ValueError("Not currently this player's turn")

        if player != self.current_turn.p:
            raise ValueError("Not this player's turn")

        suggestion = Suggestion(aTurnOrder= self.turnOrder)
        disprovePlayer, disproveHand = suggestion.makeSuggestion(aSuspect,aWeapon,aRoom)

        return disprovePlayer, disproveHand

    def handle_accusation(self, suspect: str, weapon: str, room: str) -> bool:
        """Handle an accusation from a player."""
        # Eliminate player
        current_turn = self.turnOrder.get_current_turn()
        if current_turn:
            accusation = Accusation(self.case_file)
            # Check if Accusation was correct
            if accusation.makeAccusation(suspect, weapon, room):
                self.winner = current_turn
                self.state = GameState.GAME_OVER
                return True
            else:
                # TODO: Consider moving is_game_over() function to the
                # consumer.py and changing it name. 
                current_turn.set_player_eliminated(True)
                self.is_game_over()
                return False
        return False
    
    def is_game_over(self) -> bool:
        # Check if game is over
        active_players = self.turnOrder.get_turn_order()
        if active_players < 2:
            self.state = GameState.GAME_OVER

    def end_turn(self):
        """End current turn and start next player's turn."""
        self.turnOrder.advance_turn()


    def get_valid_moves(self, player: Player) -> List[Space]:
        """Get valid moves for a player."""
        if player != self.current_turn.p:
            return []
        return player.get_valid_moves()

    def move_player(self, player: Player, target_space: Space) -> bool:
        """Move a player to a new space."""
        if player != self.current_turn.p or not self.current_turn.isActive:
            return False

        if target_space not in self.get_valid_moves(player):
            return False

        player.prevLocation = player.get_current_location()
        player.set_current_location(target_space)
        return True
    
    def get_game_winner(self) -> Player:
        return self.winner
    
    def get_current_player(self) -> Player:
        return self.turnOrder.get_current_turn()
 
    def handle_disprove(self, aDisprover: Player, aDisproveCard: Card):
        # TODO: let the current_player see the disprove card
        # TODO: broadcast the event (not the card) to all players
        pass
    def get_case_file(self) -> Hand:
        return self.case_file
 
    def get_valid_actions(self) -> List[Actions]:
        return self.current_turn.get_valid_actions()

    def get_turn_order(self) -> list[str]:
        active_players = self.turnOrder.get_turn_order()
        toReturn = []
        for player in active_players:
            toReturn.append(player.__str__())
        return toReturn

    def get_space_by_name(self, dest: str):
        return self.game_board.get_space_by_name(dest)
