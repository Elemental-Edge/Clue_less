from random import choice
from enum import Enum, auto
from typing import List, Optional
from Backend.cardGroupings.Card import Card, CardType
from Backend.cardGroupings.Deck import Deck
from Backend.cardGroupings.Hand import Hand
from Backend.gameboardGroupings.gameboard import GameBoard
from Backend.gameboardGroupings.space import Space
from Backend.gameboardGroupings.turn_order import TurnOrder
from Backend.GameManagement.playerGroupings.Actions import (
    Accusation,
    Actions,
    Suggestion,
    Move
)
from Backend.GameManagement.playerGroupings.player import Player
from Backend.commons import ValidRooms, ValidSuspect, ValidWeapons


MIN_PLAYERS = 3
MIN_ACTIVATE_PLAYERS = 2
MAX_PLAYERS = 6


class GameState(Enum):
    """Enum that represents the game status"""

    OPEN = auto()
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
        # min players required to start the game
        self._max_players: int = max_players
        # max player a gam can have
        self._min_activate_players: int = min_activate_players
        self._available_characters: List[str] = [
            suspect.value for suspect in ValidSuspect
        ]
        self._player_lobby_count: int = 0
        # tracks number of players in the game lobby


        # Game components
        self._game_board: GameBoard = GameBoard()
        # creates gameboard, which builds the gameboard for the game
        # and provides functionality to select spaces and sets default game_spaces
        self._main_deck: Deck = Deck()
        # creates a deck to store all the cards in the game
        self._case_file: Hand = Hand()
        # creates a hand that stores the case file

        # Game state
        self._game_status: GameState = GameState.OPEN
        self._winner: Player = None
        self._players_choosing_character = 0

        self._turn_order: TurnOrder = TurnOrder()
        # initializes the turn order
        self._initialize_deck()
        # initializes the deck

        # Set starting position
        self._game_board.set_starting_positions()

        for player in self._available_characters:
            player_to_add = Player(player, -1)
            player_to_add.set_current_location(self._game_board.get_starting_position(player_to_add.get_character()))
            self._turn_order.add_player(player_to_add)

    def __str__(self):
        return self._game_status

    def _initialize_deck(self) -> None:
        """Initialize the main deck with all cards."""
        # Add all suspect cards
        for suspect in ValidSuspect:
            self._main_deck.add_card(Card(suspect.value, CardType.SUSPECT))

        # Add all weapon cards
        for weapon in ValidWeapons:
            self._main_deck.add_card(Card(weapon.value, CardType.WEAPON))

        # Add all room cards
        for room in ValidRooms:
            self._main_deck.add_card(Card(room.value, CardType.ROOM))
    
    def _create_case_file(self):
        """Create the case file by selecting one of each card type."""
        self._main_deck.shuffle()

        # Get one of each type
        suspect = choice([card for card in self._main_deck.get_deck()
                         if card.get_card_type() == CardType.SUSPECT])
        weapon = choice([card for card in self._main_deck.get_deck()
                        if card.get_card_type() == CardType.WEAPON])
        room = choice([card for card in self._main_deck.get_deck()
                      if card.get_card_type() == CardType.ROOM])
        print(f"{suspect.__str__()} {weapon.__str__()} {room.__str__()}")

        # Remove from main deck and add to case file
        for card in [suspect, weapon, room]:
            self._main_deck.remove_card(card)
            self._case_file.add_card(card)

    def _deal_cards(self):
        """Deal remaining cards to players."""
        self._main_deck.shuffle()
        while not self._main_deck.is_empty():
            for player in self._turn_order:
                card = self._main_deck.deal()
                if card is None:
                    break
                player.receive_card_dealt(card)

    def add_player(self, player_name: str, player_id: int):
        """Add a new player to the game."""
        if self._game_status != GameState.OPEN:
            raise ValueError("Cannot add players after game has started")

        if self._turn_order.get_player_count() + 1 > self._max_players:
            raise ValueError(
                "Maximum number of players reached," "cannot join the game"
            )

        # Create new player
        print(f"player_name: {player_name}")
        playerObj = self._turn_order.get_player_object(player_name)
        print(f"player object: {playerObj}")
        playerObj.set_player_id(player_id)
        playerObj.set_active()
        print(f"player_lobby_count {self._player_lobby_count}")
        self._player_lobby_count += 1

    def remove_player(self, player_id: int):
        player = self._turn_order.get_player(player_id)
        player.set_player_id(-1)
        player.set_active(False)
        if not player:
            raise ValueError(f"Player with ID {player_id} not found.")
        self._turn_order.remove_player(player_id)

    def set_character_for_player(self, player_id: int, character_name: str):
        player = self._turn_order.get_player(player_id)
        if player is None:
            raise ValueError(f"Player with ID {player_id} not found.")

        if player.character_name is not None and player.get_character() != character_name:

            if not character_name in self._available_characters:
                raise ValueError(f"Character {character_name} is not available.")
            else:
                self._available_characters.append(player.get_character())


        if character_name not in self._available_characters:
            raise ValueError(f"Character {character_name} is not available.")
        player.set_character()

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


    def start_game(self):
        """Initialize and start the game."""
        if self._turn_order.get_player_count() < self._min_players:
            raise ValueError(f"Need at least {self._min_players} players to start")
        if self._turn_order.get_player_count() % self._min_players != 0:
            raise ValueError(
                f"{self._turn_order.get_player_count()} players, must have a multiple of {self._min_players} players to start."
            )

        self._game_status = GameState.INITIALIZING

        # Create case file
        self._create_case_file()

        # Deal remaining cards
        self._deal_cards()

        self._turn_order.randomize_order()

        # Start first turn
        self._game_status = GameState.IN_PROGRESS
            
    def handle_suggestion(
        self, player: Player, aSuspect: str, aWeapon: str, aRoom: str
    ) -> Optional[tuple[Player, Hand]]:
        """Handle a suggestion from a player."""
        current_turn = self._turn_order.get_current_turn()
        if not current_turn:
            raise ValueError("Not currently this player's turn")

        target_space = self._game_board.get_space_by_name(aRoom)
        suggestion = Suggestion(self._turn_order)
        disprovePlayer, disproveHand = suggestion.makeSuggestion(
            aSuspect, aWeapon, aRoom, target_space
        )

        return disprovePlayer, disproveHand

    def handle_accusation(self, suspect: str, weapon: str, room: str) -> bool:
        """Handle an accusation from a player."""
        # Eliminate player
        current_turn = self._turn_order.get_current_turn()
        if current_turn:
            accusation = Accusation(self._turn_order, self._case_file)
            # Check if Accusation was correct
            if accusation.makeAccusation(suspect, weapon, room):
                self._winner = current_turn
                self._game_status = GameState.GAME_OVER
                return True
            else:
                # TODO: Consider moving is_game_over() function to the
                # consumer.py and changing it name.
                current_turn.set_eliminated(True)
                self.is_game_over()
                return False
        return False

    def is_game_status_in_game(self) -> bool:
        return GameState.IN_PROGRESS == self._game_status or GameState.INITIALIZING == self._game_status

    def is_game_over(self) -> bool:
        # Check if game is over
        active_players = self._turn_order.get_player_count()
        if active_players < self._min_activate_players:
            self._game_status = GameState.GAME_OVER
            return True
        return False
        

    def end_turn(self):
        """End current turn and start next player's turn."""
        self._turn_order.advance_turn()

    def get_valid_moves(self, player: Player) -> List[Space]:
        """Get valid moves for a player."""
        valid_moves = []
        print("before player equality check line 275 gameprocessor")
        if player == self._turn_order.get_current_turn():
            print("after equality check")
            valid_moves = player.get_valid_moves()

        print("length of valid moves", len(valid_moves))
        return valid_moves

    def handle_move(self, player: Player, atargetSpace: str) -> bool:
        """Move a player to a new space."""
        #TODO: Update to make move
        current_player = self._turn_order.get_current_turn()
        if player != current_player:
            return False
        target_space = self._game_board.get_space_by_name(atargetSpace)
        print("player", player.get_character())
        print("target_space", target_space.__str__())
        if None is not target_space and target_space not in self.get_valid_moves(player):
            return False

        move = Move(self._turn_order)
        # Check if Accusation was correct
        return None is not move and move.makeMove(target_space)


    def get_game_winner(self) -> Player:
        return self._winner

    def get_current_player(self) -> Player:
        return self._turn_order.get_current_turn()

    def get_case_file(self) -> Hand:
        return self._case_file

    def get_valid_actions(self) -> List[str]:
        return self._turn_order.get_current_turn().get_player_turn().get_valid_actions()

    def get_turn_order(self) -> list[str]:
        active_players = self._turn_order.get_turn_order()
        toReturn = []
        for player in active_players:
            toReturn.append(player.__str__())
        return toReturn

    def get_space_by_name(self, dest: str):
        return self._game_board.get_space_by_name(dest)

    def get_game_status(self) -> int:
        return self._game_status

    def get_game_status_str(self) -> str:
        return str(self._game_status)

    def get_player_count(self) -> int:
        return self._turn_order.get_player_count()

    def get_player_choosing_characters_count(self) -> int:
        return self._players_choosing_character

    def choosing_characters_count_plus(self) -> int:
        self._players_choosing_character = self._players_choosing_character + 1
        return self._players_choosing_character

    def choosing_characters_count_minus(self) -> int:
        self._players_choosing_character = self._players_choosing_character - 1
        return self._players_choosing_character

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

    def set_game_status(self, game_status: int | GameState) -> bool:
        pass

    def is_space_to_join(self):
        return self._turn_order.get_player_count() >= self._max_players

    def can_join(self) -> bool:
        pass

    def get_player_lobby_count(self) -> int:
        return self._player_lobby_count

    def set_player_lobby_count(self, count: int):
        pass

    def increment_lobby_count(self) -> int:
        pass

    def decrement_lobby_count(self) -> int:
        pass
