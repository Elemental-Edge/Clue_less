from random import choice
from enum import Enum, auto
from typing import List, Optional
from Backend.cardGroupings.Card import Card, CardType
from Backend.cardGroupings.Deck import Deck
from Backend.cardGroupings.Hand import Hand
from Backend.gameboardGroupings.gameboard import GameBoard
from Backend.gameboardGroupings.space import Space
from Backend.gameboardGroupings.turn_order import TurnOrder
from Backend.GameManagement.playerGroupings.Actions import (Accusation,
                                                            Actions,
                                                            Suggestion)
from Backend.GameManagement.playerGroupings.player import Player
from Backend.commons import ValidRooms, ValidSuspect, ValidWeapons


MIN_PLAYERS = 3
MAX_PLAYERS = 6
MIN_ACTIVATE_PLAYERS = 2


class GameStatus(Enum):
    """Enum that represents the game status"""
    OPEN = auto()


class GameState(Enum):
    WAITING_FOR_PLAYERS = auto()
    INITIALIZING = auto()
    IN_PROGRESS = auto()
    GAME_OVER = auto()

    def __str__(self):
        """Calling the str() function on the GameStatus enum returns a string
        that represents the Game Status.
        """
        # Returns the GameStatus Name
        return self.name.replace("_", " ").title()


class GameProcessor:
    """Controls the game flow and manages game state."""

    def __init__(
        self,
        game_id: str,
        min_players: int = MIN_PLAYERS,
        max_players: int = MAX_PLAYERS,
        min_activate_players: int = MIN_ACTIVATE_PLAYERS,
    ):

        # Game identification
        self._game_id: str = game_id

        # Game settings
        self._min_players: int = min_players
        self._max_players: int = max_players
        self._min_activate_players: int = min_activate_players
        self._available_characters: List[str] = Card.VALID_SUSPECTS
        # Game components
        self._game_board: GameBoard = GameBoard()
        self._main_deck: Deck = Deck()
        self._case_file: Hand = Hand()

        # Game state
        self.game_status: GameStatus = GameStatus.OPEN
        self._winner: Player = None

        self._turn_order: TurnOrder = TurnOrder()
        self._initialize_deck()

    def __str__(self):
        return self.game_status

    def _initialize_deck(self) -> None:
        """Initialize the main deck with all cards."""
        # Add all suspect cards
        for suspect in ValidSuspect:
            self.main_deck.add_card(Card(suspect, CardType.SUSPECT))

        # Add all weapon cards
        for weapon in ValidWeapons:
            self.main_deck.add_card(Card(weapon, CardType.WEAPON))

        # Add all room cards
        for room in ValidRooms:
            self.main_deck.add_card(Card(room, CardType.ROOM))

    def add_player(self, player_name: str, player_id: int) -> bool:
        """Add a new player to the game."""
        if self.game_status != GameStatus.OPEN:
            raise ValueError("Cannot add players after game has started")

        if self._turn_order.get_player_count() + 1 > self._max_players:
            raise ValueError("Maximum number of players reached, cannot join the game")

        # Create new player
        player = Player(player_name, player_id)
        # TODO: review this function to determine if it can be simplified

        # Set starting position
        starting_positions = self._game_board.get_starting_positions()
        player._currLocation = starting_positions[player._character]

        self._turn_order.add_player(player)

    def start_game(self):
        """Initialize and start the game."""
        if self._turn_order.get_player_count() < self._min_players:
            raise ValueError(f"Need at least {self._min_players} players to start")
        if self._turn_order.get_player_count() % self._min_players != 0:
            raise ValueError(
                f"{self._turn_order.get_player_count()} players, must have a multiple of {self._min_players} players to start."
            )

        self.game_status = GameStatus.INITIALIZING

        # Create case file
        self._create_case_file()

        # Deal remaining cards
        self._deal_cards()

        self._turn_order.randomize_order()

        # Start first turn
        self.game_status = GameStatus.IN_PROGRESS

    def _create_case_file(self) -> None:
        """Create the case file by selecting one of each card type."""
        self._main_deck.shuffle()

        # Get one of each type
        suspect = next(
            card
            for card in self._main_deck.get_deck()
            if card.get_card_type() == CardType.SUSPECT
        )
        weapon = next(
            card
            for card in self._main_deck.get_deck()
            if card.get_card_type() == CardType.WEAPON
        )
        room = next(
            card
            for card in self._main_deck.get_deck()
            if card.get_card_type() == CardType.ROOM
        )

        # Remove from main deck and add to case file
        for card in [suspect, weapon, room]:
            self._main_deck.remove_card(card)
            self._case_file.add_card(card)

    def _deal_cards(self) -> None:
        """Deal remaining cards to players."""
        self._main_deck.shuffle()

        # Deal all remaining cards
        for card in self._main_deck.get_deck():
            self._turn_order.advance_turn()
            current_turn = self._turn_order.get_current_turn()
            # sets current players turn
            if current_turn:
                current_turn.receive_card_dealt(card)

    def handle_suggestion(
        self, player: Player, aSuspect: str, aWeapon: str, aRoom: str
    ) -> Optional[tuple[Player, Hand]]:
        """Handle a suggestion from a player."""
        if not self.current_turn or not self.current_turn.isActive:
            raise ValueError("Not currently this player's turn")

        if player != self.current_turn.p:
            raise ValueError("Not this player's turn")

        suggestion = Suggestion(self._turn_order)
        disprovePlayer, disproveHand = suggestion.makeSuggestion(
            aSuspect, aWeapon, aRoom
        )

        return disprovePlayer, disproveHand

    def handle_accusation(self, suspect: str, weapon: str, room: str) -> bool:
        """Handle an accusation from a player."""
        # Eliminate player
        current_turn = self._turn_order.get_current_turn()
        if current_turn:
            accusation = Accusation(self._case_file)
            # Check if Accusation was correct
            if accusation.makeAccusation(suspect, weapon, room):
                self._winner = current_turn
                self.game_status = GameStatus.GAME_OVER
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
        active_players = self._turn_order.get_active_player_count()
        if active_players < self.MIN_ACTIVATE_PLAYERS:
            self.game_status = GameStatus.GAME_OVER

    def end_turn(self):
        """End current turn and start next player's turn."""
        self._turn_order.advance_turn()

    def get_valid_moves(self, player: Player) -> List[Space]:
        """Get valid moves for a player."""
        valid_moves = []
        if player == self._turn_order.get_current_turn():
            valid_moves = player.get_valid_moves()
        return valid_moves

    def move_player(self, player: Player, target_space: Space) -> bool:
        """Move a player to a new space."""
        if player != self.current_turn.p or not self.current_turn.isActive:
            return False

        if target_space not in self.get_valid_moves(player):
            return False

        player._prevLocation = player.get_current_location()
        player.set_current_location(target_space)
        return True

    def get_game_winner(self) -> Player:
        return self._winner

    def get_current_player(self) -> Player:
        return self._turn_order.get_current_turn()

    def get_case_file(self) -> Hand:
        return self._case_file

    def get_valid_actions(self) -> List[Actions]:
        return self.current_turn.get_valid_actions()

    def get_turn_order(self) -> list[str]:
        active_players = self._turn_order.get_turn_order()
        toReturn = []
        for player in active_players:
            toReturn.append(player.__str__())
        return toReturn

    def get_space_by_name(self, dest: str):
        return self._game_board.get_space_by_name(dest)

    def get_game_status(self) -> int:
        return self.game_status

    def get_game_status_str(self) -> str:
        return str(self.game_status)

    def get_player_count(self) -> int:
        return self._turn_order.get_player_count()

    def get_max_players(self) -> int:
        return self._max_players

    def get_min_players(self) -> int:
        return self._min_players

    def get_min_activate_players(self) -> int:
        return self._min_activate_players

    def get_available_characters(self) -> List[str]:
        return self._available_characters

    def get_selected_characters(self) -> List[str]:
        return [player.get_character() for player in self._turn_order]

    def set_character(self, player_id: int, character_name: str) -> bool:
        is_success = False
        # POTENTIAL BUG: if the character_name attempting to be set is the
        # same as current players character the function will return false
        player = self._turn_order.get_player(player_id)
        if player is not None:
            # assumes that a plyaers character is valid
            if player.character is not None and player.character != character_name:
                self._available_characters.append(player.character)
                if character_name in self._available_characters:
                    player.set_character(character_name)
                    # TODO: modify the function to be agnostic of type
                    # may be a bad idea to try and remove via string
                    self._available_characters.remove(character_name)
                    is_success = True
        return is_success

    def set_random_character(self, player_id: int):
        is_success = True
        player = self._turn_order.get_player(player_id)
        if player is not None:
            if player.character is not None:
                # BUG: assumes player.character is not ""
                self._available_characters.append(player.character)
                selected_character = choice(self._available_characters)
                # BUG: assumes a unselected character exists
                player.set_character(selected_character)
                is_success = True
        return is_success

    def set_game_status(self, game_status: int | GameStatus) -> bool:
        pass

    def is_space_to_join(self):
        return self._turn_order.get_player_count() >= self._max_players

    def can_join(self) -> bool:
        pass
