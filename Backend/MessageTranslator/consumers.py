import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from GameManagement.models import GameRoom
from channels.generic.websocket import WebsocketConsumer
from django.db import transaction


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    A WebSocket consumer for handling real-time notifications.

    This class manages WebSocket connections for sending notifications to clients.
    It allows clients to connect to a notification group and receive messages in real-time.

    Methods:
        connect(): Accepts the WebSocket connection and joins the notifications group.
        disconnect(close_code): Leaves the notifications group upon disconnection.
        notify(event): Sends a notification message to the WebSocket client.
    """
    async def connect(self):
        """
        Handle WebSocket connection requests.

        This method is called when a client connects to the WebSocket.
        It adds the client to the 'notifications' group and accepts the connection.
        """
        try:
            self.channel_layer = get_channel_layer()  # Get the channel layer
            await self.channel_layer.group_add("notifications", self.channel_name)  # Join the notifications group
            await self.accept()  # Accept the WebSocket connection
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error while connecting to notifications group: {e}")

    async def disconnect(self, close_code: int) -> None:
        """
        Handle WebSocket disconnection requests.

        This method is called when a client disconnects from the WebSocket.
        It removes the client from the 'notifications' group.

        Args:
            close_code (int): The code indicating why the WebSocket connection was closed.
        """
        try:
            await self.channel_layer.group_discard("notifications", self.channel_name)  # Leave the notifications group
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error while disconnecting from notifications group: {e}")

    async def notify(self, event: dict) -> None:
        """
        Send a notification message to the WebSocket client.

        This method is called when a notification event occurs. It sends the message
        contained in the event to the connected WebSocket client.

        Args:
            event (dict): The event dictionary containing the notification message.
        """
        try:
            message = event['message']  # Extract the message from the event
            await self.send(text_data=json.dumps({'message': message}))  # Send the notification message to WebSocket
        except KeyError:
            print("Notification event does not contain 'message' key.")
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error while sending notification: {e}")



class GameRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        
        if not self.user.is_authenticated:
            self.close()
            return

        # Get game room and validate
        self.game_room = self.get_room()
        if not self.game_room:
            self.close()
            return

        if not self.can_join():
            self.close()
            return

        # Join game group
        self.channel_layer.group_add(
            f"game_{self.game_id}",
            self.channel_name
        )

        # Get or create game processor
        self.game_manager = GameManager.get_instance()
        self.game_processor = self.game_manager.get_game(str(self.game_id))
        
        if not self.game_processor:
            if self.is_host():
                self.game_processor = self.game_manager.create_game(self.game_room)
            else:
                self.close()
                return

        # Add player to game
        self.add_player_to_game()
        self.accept()
        
        # Send initial game state
        self.send_game_state()

    def get_room(self):
        try:
            return GameRoom.objects.get(game_id=self.game_id)
        except GameRoom.DoesNotExist:
            return None

    def can_join(self):
        can_join = (
            self.game_room.player_count < self.game_room.max_players and
            not self.game_room.status == "IN_PROGRESS"
        )
        
        if self.game_room.is_password:
            query_string = parse_qs(self.scope["query_string"].decode())
            passcode = query_string.get("passcode", [None])[0]
            can_join = can_join and passcode == self.game_room.passcode
            
        return can_join

    def is_host(self):
        return self.game_room.host == self.user

    def add_player_to_game(self):
        with transaction.atomic():
            self.game_room.player_count += 1
            self.game_room.save()
            self.game_processor.add_player(self.user.username)

    def receive(self, text_data):
        """Handle incoming WebSocket messages"""
        try:
            content = json.loads(text_data)
            action = content.get('action')
            
            if action == 'start_game' and self.is_host():
                self.handle_start_game()
            elif action == 'move':
                self.handle_move(content)
            elif action == 'suggestion':
                self.handle_suggestion(content)
            elif action == 'accusation':
                self.handle_accusation(content)
            
        except json.JSONDecodeError:
            self.send(text_data=json.dumps({
                'error': 'Invalid JSON format'
            }))

    def handle_start_game(self):
        if self.game_room.player_count >= 3:
            self.game_processor.start_game()
            
            # Update game room status
            with transaction.atomic():
                self.game_room.status = "IN_PROGRESS"
                self.game_room.save()
            
            # Notify all players
            self.channel_layer.group_send(
                f"game_{self.game_id}",
                {
                    "type": "game.started",
                    "data": self.game_processor.get_game_state()
                }
            )

    def handle_move(self, content):
        if not self.is_current_player():
            return
            
        space_name = content.get('space')
        player = self.game_processor.get_player_by_name(self.user.username)
        
        if self.game_processor.move_player(player, space_name):
            self.channel_layer.group_send(
                f"game_{self.game_id}",
                {
                    "type": "game.move",
                    "player": self.user.username,
                    "space": space_name
                }
            )

    def handle_suggestion(self, content):
        if not self.is_current_player():
            return
            
        player = self.game_processor.get_player_by_name(self.user.username)
        result = self.game_processor.handle_suggestion(
            player,
            content.get('suspect'),
            content.get('weapon'),
            content.get('room')
        )
        
        # Send result only to suggesting player
        self.send(text_data=json.dumps({
            'type': 'suggestion_result',
            'card': result.get_name() if result else None
        }))

    def handle_accusation(self, content):
        if not self.is_current_player():
            return
            
        player = self.game_processor.get_player_by_name(self.user.username)
        result = self.game_processor.handle_accusation(
            player,
            content.get('suspect'),
            content.get('weapon'),
            content.get('room')
        )
        
        if result:
            self.handle_game_over(self.user.username)
        else:
            # Notify only the accusing player
            self.send(text_data=json.dumps({
                'type': 'accusation_result',
                'success': False
            }))

    def handle_game_over(self, winner):
        self.channel_layer.group_send(
            f"game_{self.game_id}",
            {
                "type": "game.over",
                "winner": winner
            }
        )
        self.update_user_stats(winner == self.user.username)

    def is_current_player(self):
        return (
            self.game_processor and 
            self.game_processor.current_turn and 
            self.game_processor.current_turn.p.playerName == self.user.username
        )

    def disconnect(self, close_code):
        if hasattr(self, 'game_id'):
            self.channel_layer.group_discard(
                f"game_{self.game_id}",
                self.channel_name
            )
            
        if hasattr(self, 'game_room'):
            self.remove_player_from_game()

    def remove_player_from_game(self):
        with transaction.atomic():
            self.game_room.player_count = max(0, self.game_room.player_count - 1)
            self.game_room.save()
            if self.game_room.player_count == 0:
                GameManager.get_instance().remove_game(str(self.game_id))

    def update_user_stats(self, won: bool):
        stats, _ = UserStats.objects.get_or_create(user=self.user)
        if won:
            stats.add_win()
        else:
            stats.add_loss()
        stats.calculate_session_time()

    def send_game_state(self):
        """Send current game state to the connecting player"""
        if self.game_processor:
            self.send(text_data=json.dumps({
                'type': 'game_state',
                'data': self.game_processor.get_game_state()
            }))

    # Channel layer message handlers
    def game_started(self, event):
        self.send(text_data=json.dumps(event))

    def game_move(self, event):
        self.send(text_data=json.dumps(event))

    def game_over(self, event):
        self.send(text_data=json.dumps(event))