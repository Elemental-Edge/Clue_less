from typing import Dict, Optional
from channels.layers import get_channel_layer
import asyncio

class GameManager:
    """Singleton class to manage active games in memory"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.active_games: Dict[str, GameProcessor] = {}
        self.player_to_game: Dict[str, str] = {}  # username -> game_id

    def create_game(self, game_room: GameRoom) -> GameProcessor:
        """Create a new game processor for a game room"""
        game_id = str(game_room.game_id)
        processor = GameProcessor()
        self.active_games[game_id] = processor
        return processor

    def get_game(self, game_id: str) -> Optional[GameProcessor]:
        """Get an active game processor"""
        return self.active_games.get(game_id)

    def remove_game(self, game_id: str):
        """Remove a game and its player mappings"""
        if game_id in self.active_games:
            # Remove player mappings for this game
            self.player_to_game = {
                username: gid 
                for username, gid in self.player_to_game.items() 
                if gid != game_id
            }
            del self.active_games[game_id]

    def add_player_to_game(self, username: str, game_id: str):
        """Map a player to a game"""
        self.player_to_game[username] = game_id

    def remove_player_from_game(self, username: str):
        """Remove a player's game mapping"""
        self.player_to_game.pop(username, None)

    def get_player_game(self, username: str) -> Optional[str]:
        """Get a player's current game ID"""
        return self.player_to_game.get(username)