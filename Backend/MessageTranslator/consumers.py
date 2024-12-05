import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.generic.websocket import WebsocketConsumer
from django.db import transaction
from django.http import JsonResponse
from..GameManagement.models import GameRoom
from asgiref.sync import sync_to_async
from Backend.gameboardGroupings.game_processor import GameProcessor
import re
import string
import uuid


class NotificationConsumer(AsyncWebsocketConsumer):
    gamerooms = []

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


    async def receive(self, text_data):
        try:
            # Parse the incoming WebSocket message
            command = text_data.split()
            c = command[0];
            match c:

                # CREATE GAME
                case "create-game":

                    try:
                        if self.scope["session"].get("_auth_user_id", None) == None:
                            await self.send(json.dumps({
                                "error": "You are not logged in and therefore cannot create a game."
                            }))

                        # get session
                        session = self.scope["session"]

                        await self.send(json.dumps({
                            "c": 0
                        }))

                        # create game room
                        name = f"{session['_auth_username']}'s Game";
                        game = GameRoom(
                            name = name,
                            player_count = 1,
                            max_players = 6
                        )

                        await self.send(json.dumps({
                            "c": 1
                        }))

                        # update session
                        session['_game_id'] = game.generate_game_id()
                        gamechannel = f"game-{session['_game_id']}"
                        session['_game_channel'] = gamechannel

                        await self.send(json.dumps({
                            "c": 2
                        }))


                        # add this user to game channel
                        await self.channel_layer.group_add(
                            gamechannel,  # Group name
                            self.channel_name  # The user's unique channel
                        )

                        await self.send(json.dumps({
                            "c": 3
                        }))


                        # remove user from game selection
                        await self.channel_layer.group_discard(
                            "gameslobby",  # Group name
                            self.channel_name  # The user's unique channel
                        )

                        # save game then session
                        await sync_to_async(game.save)()
                        await sync_to_async(session.save)()

                        await self.channel_layer.group_send(
                            "gameslobby",
                            json.dumps({
                                "command": "add-game-to-list",
                                "name": name,
                                "id": session['_game_id']
                            })
                        )

                        return await self.send(json.dumps({
                            "command": "successful-create-game",
                            "name": name,
                            "id": session['_game_id']
                        }))

                    
                    except Exception as e:
                        print(f"Unknown login error with command: {e}")
                        return await self.send(json.dumps({
                            "error": "Unknown create game error."
                        }))
                
                # LOGIN
                case "login":

                    try:
                        username = command[1]
                        password = command[2]

                        # Authenticate user
                        from django.contrib.auth import authenticate
                        user = await sync_to_async(authenticate)(username=username, password=password)

                        if user is not None:

                            session = self.scope["session"]
                            session["_auth_user_id"] = user.id
                            session["_auth_username"] = user.username
                            user.backend = 'django.contrib.auth.backends.ModelBackend'
                            session['_auth_user_backend'] = user.backend

                            # Save the session (wrapped in sync_to_async)
                            await sync_to_async(session.save)()

                            # Add user to gameslobby channel
                            await self.channel_layer.group_add(
                                "gameslobby",  # Group name
                                self.channel_name  # The user's unique channel
                            )

                            await self.send(json.dumps({
                                "command": "successful-login",
                                "username": session["_auth_username"]
                            }))

                        else:
                            # bad username/password combo
                            await self.send(json.dumps({
                                "command": "set-text-and-unhide",
                                "selector": "#login-popup-error",
                                "text": "Bad username/password combination."
                            }))
                    
                    except Exception as e:
                        
                        if (len(command) != 3):
                            await self.send(json.dumps({
                                    "command": "set-text-and-unhide",
                                    "selector": "#login-popup-error",
                                    "text": "Please type a username and password."
                            }))

                        else:
                            print(f"Unknown login error with command: {e}")
                            await self.send(json.dumps({
                                    "command": "set-text-and-unhide",
                                    "selector": "#login-popup-error",
                                    "text": "Unknown login error."
                            }))

                    return;
                

                # REGISTER
                case "register":

                    try:
                        username = command[1]
                        password = command[2]
                        confirm = command[3]

                        # Validate username
                        # Check if username is alphanumeric
                        if (not username.isalnum()) or len(username) < 3:
                            return await self.send(json.dumps({
                                "command": "set-text-and-unhide",
                                "selector": "#register-popup-error",
                                "text": "Username must be alphanumeric and at least 3 digits."
                            }))

                        # Check if username is already taken
                        from django.contrib.auth.models import User
                        if await sync_to_async(User.objects.filter(username=username).exists)():
                            return await self.send(json.dumps({
                                "command": "set-text-and-unhide",
                                "selector": "#register-popup-error",
                                "text": "That username is already taken."
                            }))
                        
                        # Validate password
                        # Check if passwords match
                        if password != confirm:
                            return await self.send(json.dumps({
                                "command": "set-text-and-unhide",
                                "selector": "#register-popup-error",
                                "text": "Passwords do not match."
                            }))

                        # Check password length
                        if len(password) < 8:
                            return await self.send(json.dumps({
                                "command": "set-text-and-unhide",
                                "selector": "#register-popup-error",
                                "text": "Passwords must be at least 8 characters long."
                            }))

                        # Check for spaces
                        if len(password) < 8 or any(char.isspace() for char in password) or not all(char in string.printable for char in password):
                            return await self.send(json.dumps({
                                "command": "set-html-and-unhide",
                                "selector": "#register-popup-error",
                                "html": "Password must be at least 8 characters long,<br />must not contain spaces, tabs, or returns<br />and may only contain other ASCII characters."
                            }))
                        
                        # Create User
                        user = await sync_to_async(User.objects.create_user)(username=username, password=password)
                        await sync_to_async(user.save)()

                        session = self.scope["session"]
                        session["_auth_user_id"] = user.id
                        session["_auth_username"] = user.username
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        session['_auth_user_backend'] = user.backend

                        # Save the session (wrapped in sync_to_async)
                        await sync_to_async(session.save)()

                        # Add user to gameslobby channel
                        await self.channel_layer.group_add(
                            "gameslobby",  # Group name
                            self.channel_name  # The user's unique channel
                        )

                        return await self.send(json.dumps({
                            "command": "successful-register",
                            "username": session["_auth_username"]
                        }))

                    except Exception as e:

                        if (len(command) != 4):
                            await self.send(json.dumps({
                                    "command": "set-text-and-unhide",
                                    "selector": "#register-popup-error",
                                    "text": "Please type a username, password, and confirm your password."
                            }))

                        else:
                            print(f"Unknown register error with command: {e}")
                            await self.send(json.dumps({
                                    "command": "set-text-and-unhide",
                                    "selector": "#register-popup-error",
                                    "text": "Unknown register error."
                            }))

                    return;
                
                # show/update dealt cards
                case "showDealtCards":
                    session = self.scope["session"]
                    await sync_to_async(session.save)()

                    return await self.send(json.dumps({
                        "command": "show-dealt-cards"
                        "cards": GameProcessor.get_current_player.get_hand().toString()  # TODO: need to implement toString for Hand and get_hand() method in player
                    }))

                # get valid actions list for current player
                case "getValidActions":
                    actions_list = GameProcessor.get_valid_actions()

                    session = self.scope["session"]
                    await sync_to_async(session.save)()

                    return await self.send(json.dumps({
                        "command": "show-valid-actions"
                        "actions": actions_list.toString()  # TODO: need to implement toString for Actions
                    }))

                case "makeAccusation":
                    suspect = command[1]
                    weapon = command[2]
                    room = command[3]
                    result = GameProcessor.handle_accusation(GameProcessor.get_current_player(), suspect, weapon, room)

                    session = self.scope["session"]
                    await sync_to_async(session.save)()

                    if result:
                        return await self.send(json.dumps({
                            "command": "win"
                            "winner": GameProcessor.get_current_player()   # TODO: need to implement get_current_player() in GameProcessor
                            "winningCards": suspect, weapon, room  # TODO: need to implement toString for Hand
                        }))
                    else:
                        # send eliminated player information
                        return await self.send(json.dumps({
                            "command": "eliminate"
                            "eliminated": GameProcessor.get_current_player()   # TODO: need to implement get_current_player() in GameProcessor
                        }))

                case "makeSuggestion":
                    suspect = command[1]
                    weapon = command[2]
                    room = command[3]
                    (disprover, disproveCards) = GameProcessor.handle_suggestion(GameProcessor.get_current_player(), suspect, weapon, room)
                    
                    session = self.scope["session"]
                    await sync_to_async(session.save)()

                    # TODO: cannot-disprove popup, unhide for other players

                    return await self.send(json.dumps({
                        "command": "disprove-select"
                        "disprover": disprover.toString()   # TODO: need to implement toString for Player
                        "disproveCards": disproveCards.toString()  # TODO: need to implement toString for Hand
                    }))

                case "disproveReceived":
                    disprover = command[1]
                    disproveCard = command[2]
                    # TODO: end current user's turn and update to next player turn
                    GameProcessor.handle_disprove(disprover, disproveCard)  # TODO: need to implement this method
                    GameProcessor.end_turn()
             
                # unknown case
                case _:
                    await self.send(json.dumps({
                        "status": "error",
                        "message": f"There is no {c} commmand."
                    }))

        except Exception as e:
            print(f"Error processing message: {e}")
            await self.send(json.dumps({
                "status": "error",
                "message": "Invalid request format."
            }))

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
