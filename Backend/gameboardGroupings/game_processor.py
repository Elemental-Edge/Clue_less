from enum import Enum, auto
from typing import List, Optional, Dict, Set
from cardGroupings.Deck import Deck
from cardGroupings.Hand import Hand
from cardGroupings.Card import Card, CardType
from Backend.GameManagement.playerGroupings.player import Player
from Backend.GameManagement.playerGroupings.Actions import Accusation, Suggestion
from turn_order import TurnOrder
from space import Room, Hallway, Space
import random

class GameState(Enum):
    WAITING_FOR_PLAYERS = auto()
    INITIALIZING = auto()
    IN_PROGRESS = auto()
    GAME_OVER = auto()

class GameProcessor:
    """Controls the game flow and manages game state."""

    MIN_PLAYERS = 3
    MAX_PLAYERS = 6

    def __init__(self):
        # Game identification
        self.game_id: str = str(uuid.uuid4())

        # Game components
        self.game_board: GameBoard = GameBoard()
        self.main_deck: Deck = Deck()
        self.case_file: Hand = Hand()

        # Player management
        self.players: List[Player] = []
        self.current_turn: Optional[Player_Turn] = None
        self.eliminated_players: Set[Player] = set()

        # Game state
        self.state: GameState = GameState.WAITING_FOR_PLAYERS
        self.winner: Optional[Player] = None

        TODO: Where are we going to populate the turn oder? JKL
        self.turnOrder: Optional[TurnOrder] = None
        self._initialize_deck()

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

    def add_player(self, player_name: str) -> Optional[Player]:
        """Add a new player to the game."""
        if self.state != GameState.WAITING_FOR_PLAYERS:
            raise ValueError("Cannot add players after game has started")

        if len(self.players) >= self.MAX_PLAYERS:
            raise ValueError("Maximum number of players reached")

        # Create new player
        player = Player(player_name)
        available_characters = set(Card.VALID_SUSPECTS) - {p.character for p in self.players}
        player.character = random.choice(list(available_characters))

        # Set starting position
        starting_positions = self.game_board.get_starting_positions()
        player.currLocation = starting_positions[player.character]

        self.players.append(player)
        return player

    def start_game(self) -> bool:
        """Initialize and start the game."""
        if len(self.players) < self.MIN_PLAYERS:
            raise ValueError(f"Need at least {self.MIN_PLAYERS} players to start")

        self.state = GameState.INITIALIZING

        # Create case file
        self._create_case_file()

        # Deal remaining cards
        self._deal_cards()

        # Start first turn
        self.state = GameState.IN_PROGRESS
        self.current_turn = Player_Turn(self.players[0])
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
        current_player = 0

        # Deal all remaining cards
        while True:
            card = self.main_deck.deal()
            if not card:
                break

            self.players[current_player].receive_card_dealt(card)
            current_player = (current_player + 1) % len(self.players)

    def handle_suggestion(self, player: Player, aSuspect: str, aWeapon: str, aRoom: str) -> Optional[Card]:
        """Handle a suggestion from a player."""
        if not self.current_turn or not self.current_turn.isActive:
            raise ValueError("Not currently this player's turn")

        if player != self.current_turn.p:
            raise ValueError("Not this player's turn")

        suggestion = Suggestion(aTurnOrder= self.turnOrder)
        disprovePlayer, disproveHand = suggestion.makeSuggestion(aSuspect,aWeapon,aRoom)

        # Request that the disprove player select a card from the disprove hand
        # current player sees the disproved card
        # broadcast that a disproved suggestion was made.
        # Broadcast that the turn is over

        # Check each other player's hand in order
        # start_idx = (self.players.index(player) + 1) % len(self.players)
        # for i in range(len(self.players) - 1):
        #     check_idx = (start_idx + i) % len(self.players)
        #     check_player = self.players[check_idx]

        #     # Skip eliminated players
        #     if check_player in self.eliminated_players:
        #         continue

        #     # Check player's hand for matching cards
        #     for card in suggestion_cards:
        #         if check_player.playerHand.has_card(card):
        #             return card

        return None

    def handle_accusation(self, player: Player, suspect: str, weapon: str, room: str) -> bool:
        """Handle an accusation from a player."""
        if not self.current_turn or not self.current_turn.isActive:
            raise ValueError("Not currently this player's turn")

        accusation = Accusation(self.case_file)

        # Check if Accusation was correct
        if accusation.makeAccusation(suspect, weapon, room):
            self.winner = player
            self.state = GameState.GAME_OVER
            return True
        else:
            # Eliminate player
            self.eliminated_players.add(player)

            # Check if game is over
            active_players = len(self.players) - len(self.eliminated_players)
            if active_players < self.MIN_PLAYERS: #Should this be self.MIN_PLAYERS -1 ?
                self.state = GameState.GAME_OVER

            return False

    def end_turn(self) -> Optional[Player_Turn]:
        """End current turn and start next player's turn."""
        if not self.current_turn:
            return None

        current_player_idx = self.players.index(self.current_turn.p)

        # Find next non-eliminated player
        for i in range(1, len(self.players) + 1):
            next_idx = (current_player_idx + i) % len(self.players)
            next_player = self.players[next_idx]

            if next_player not in self.eliminated_players:
                self.current_turn = Player_Turn(next_player)
                return self.current_turn

        return None

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

        player.prevLocation = player.currLocation
        player.currLocation = target_space
        return True