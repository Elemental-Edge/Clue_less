import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from ..GameManagement.models import GameRoom
from asgiref.sync import sync_to_async
import string
from django.apps import apps


class NotificationConsumer(AsyncWebsocketConsumer):
    gamerooms = []

    def __init__(self):
        self.my_app_config = apps.get_app_config("GameManagement")
        self.game_processor_instance = self.my_app_config.get_game_processor()
        super().__init__()

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
            await self.channel_layer.group_add(
                "notifications", self.channel_name
            )  # Join the notifications group
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
            await self.channel_layer.group_discard(
                "notifications", self.channel_name
            )  # Leave the notifications group
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error while disconnecting from notifications group: {e}")

    async def receive(self, text_data):
        try:
            # Parse the incoming WebSocket message
            command = text_data.split()
            print(text_data) # TEST STATEMENT
            c = command[0]
            match c:

                # CREATE GAME
                case "create-game":

                    try:
                        if self.scope["session"].get("_auth_user_id", None) == None:
                            await self.send(
                                json.dumps(
                                    {
                                        "error": "You are not logged in and therefore cannot create a game."
                                    }
                                )
                            )

                        # get session
                        session = self.scope["session"]

                        await self.send(json.dumps({"c": 0}))

                        # create game room
                        name = f"{session['_auth_username']}'s Game"
                        game = GameRoom(name=name, player_count=1, max_players=6)

                        await self.send(json.dumps({"c": 1}))

                        # update session
                        session["_game_id"] = game.generate_game_id()
                        gamechannel = f"game-{session['_game_id']}"
                        session["_game_channel"] = gamechannel

                        await self.send(json.dumps({"c": 2}))

                        # add this user to game channel
                        await self.channel_layer.group_add(
                            gamechannel,  # Group name
                            self.channel_name,  # The user's unique channel
                        )

                        await self.send(json.dumps({"c": 3}))

                        # remove user from game selection
                        await self.channel_layer.group_discard(
                            "gameslobby",  # Group name
                            self.channel_name,  # The user's unique channel
                        )

                        # save game then session
                        await sync_to_async(game.save)()
                        await sync_to_async(session.save)()

                        await self.channel_layer.group_send(
                            "gameslobby",
                            json.dumps(
                                {
                                    "command": "add-game-to-list",
                                    "name": name,
                                    "id": session["_game_id"],
                                }
                            ),
                        )

                        return await self.send(
                            json.dumps(
                                {
                                    "command": "successful-create-game",
                                    "name": name,
                                    "id": session["_game_id"],
                                }
                            )
                        )

                    except Exception as e:
                        print(f"Unknown login error with command: {e}")
                        return await self.send(
                            json.dumps({"error": "Unknown create game error."})
                        )

                # LOGIN
                case "login":

                    try:
                        username = command[1]
                        password = command[2]

                        # Authenticate user
                        from django.contrib.auth import authenticate

                        user = await sync_to_async(authenticate)(
                            username=username, password=password
                        )

                        if user is not None:

                            session = self.scope["session"]
                            session["_auth_user_id"] = user.id
                            session["_auth_username"] = user.username
                            user.backend = "django.contrib.auth.backends.ModelBackend"
                            session["_auth_user_backend"] = user.backend

                            # Save the session (wrapped in sync_to_async)
                            await sync_to_async(session.save)()

                            # Add user to gameslobby channel
                            await self.channel_layer.group_add(
                                "gameslobby",  # Group name
                                self.channel_name,  # The user's unique channel
                            )

                            await self.send(
                                json.dumps(
                                    {
                                        "command": "successful-login",
                                        "username": session["_auth_username"],
                                    }
                                )
                            )
                            # TODO: Pass Player name and ID to GameProcessor.add_player() function

                        else:
                            # bad username/password combo
                            await self.send(
                                json.dumps(
                                    {
                                        "command": "set-text-and-unhide",
                                        "selector": "#login-popup-error",
                                        "text": "Bad username/password combination.",
                                    }
                                )
                            )

                    except Exception as e:

                        if len(command) != 3:
                            await self.send(
                                json.dumps(
                                    {
                                        "command": "set-text-and-unhide",
                                        "selector": "#login-popup-error",
                                        "text": "Please type a username and password.",
                                    }
                                )
                            )

                        else:
                            print(f"Unknown login error with command: {e}")
                            await self.send(
                                json.dumps(
                                    {
                                        "command": "set-text-and-unhide",
                                        "selector": "#login-popup-error",
                                        "text": "Unknown login error.",
                                    }
                                )
                            )

                    return

                # REGISTER
                case "register":

                    try:
                        username = command[1]
                        password = command[2]
                        confirm = command[3]

                        # Validate username
                        # Check if username is alphanumeric
                        if (not username.isalnum()) or len(username) < 3:
                            return await self.send(
                                json.dumps(
                                    {
                                        "command": "set-text-and-unhide",
                                        "selector": "#register-popup-error",
                                        "text": "Username must be alphanumeric and at least 3 digits.",
                                    }
                                )
                            )

                        # Check if username is already taken
                        from django.contrib.auth.models import User

                        if await sync_to_async(
                            User.objects.filter(username=username).exists
                        )():
                            return await self.send(
                                json.dumps(
                                    {
                                        "command": "set-text-and-unhide",
                                        "selector": "#register-popup-error",
                                        "text": "That username is already taken.",
                                    }
                                )
                            )

                        # Validate password
                        # Check if passwords match
                        if password != confirm:
                            return await self.send(
                                json.dumps(
                                    {
                                        "command": "set-text-and-unhide",
                                        "selector": "#register-popup-error",
                                        "text": "Passwords do not match.",
                                    }
                                )
                            )

                        # Check password length
                        if len(password) < 8:
                            return await self.send(
                                json.dumps(
                                    {
                                        "command": "set-text-and-unhide",
                                        "selector": "#register-popup-error",
                                        "text": "Passwords must be at least 8 characters long.",
                                    }
                                )
                            )

                        # Check for spaces
                        if (
                            len(password) < 8
                            or any(char.isspace() for char in password)
                            or not all(char in string.printable for char in password)
                        ):
                            return await self.send(
                                json.dumps(
                                    {
                                        "command": "set-html-and-unhide",
                                        "selector": "#register-popup-error",
                                        "html": "Password must be at least 8 characters long,<br />must not contain spaces, tabs, or returns<br />and may only contain other ASCII characters.",
                                    }
                                )
                            )

                        # Create User
                        user = await sync_to_async(User.objects.create_user)(
                            username=username, password=password
                        )
                        await sync_to_async(user.save)()

                        session = self.scope["session"]
                        session["_auth_user_id"] = user.id
                        session["_auth_username"] = user.username
                        user.backend = "django.contrib.auth.backends.ModelBackend"
                        session["_auth_user_backend"] = user.backend

                        # Save the session (wrapped in sync_to_async)
                        await sync_to_async(session.save)()

                        # Add user to gameslobby channel
                        await self.channel_layer.group_add(
                            "gameslobby",  # Group name
                            self.channel_name,  # The user's unique channel
                        )

                        return await self.send(
                            json.dumps(
                                {
                                    "command": "successful-register",
                                    "username": session["_auth_username"],
                                }
                            )
                        )

                    except Exception as e:

                        if len(command) != 4:
                            await self.send(
                                json.dumps(
                                    {
                                        "command": "set-text-and-unhide",
                                        "selector": "#register-popup-error",
                                        "text": "Please type a username, password, and confirm your password.",
                                    }
                                )
                            )

                        else:
                            print(f"Unknown register error with command: {e}")
                            await self.send(
                                json.dumps(
                                    {
                                        "command": "set-text-and-unhide",
                                        "selector": "#register-popup-error",
                                        "text": "Unknown register error.",
                                    }
                                )
                            )

                    return

                # show/update dealt cards
                case "showDealtCards":
                    cardsStr = []
                    for card in self.game_processor_instance.get_current_player().get_hand():
                        cardsStr.append(card.__str__())

                    return await self.send(json.dumps({
                        "command": "show-dealt-cards",
                        "cards": cardsStr
                    }))

                # get valid actions list for current player
                case "getValidActions":
                    actions_list = self.game_processor_instance.get_valid_actions()

                    return await self.send(json.dumps({
                        "command": "show-valid-actions",
                        "actions": actions_list.__str__()  # TODO: need to implement toString for Actions
                    }))


                case "accusation":
                    suspect = command[1]
                    weapon = command[2]
                    room = command[3]

                    # TODO: Add a check to ensure that requesting user is the current player
                    # i.e. selected_character == self.game_processor_instance.get_current_player()
                    result = self.game_processor_instance.handle_accusation(suspect, weapon, room)

                    # TODO: Anytime the gamestate changes need to broadcast message to clients
                    if result:
                        # also need to enter win game state on back-end in addition to win popup
                        winCards = [suspect, weapon, room]
                        return await self.send(json.dumps({
                            "command": "win",
                            "winner": self.game_processor_instance.get_current_player().__str__(),
                            "winningCards": winCards
                        }))
                    else:
                        # also need to eliminate player on backend in addition to lose popup
                        # send eliminated player information
                        return await self.send(json.dumps({
                            "command": "eliminate",
                            "eliminated": self.game_processor_instance.get_current_player().__str__()
                        }))

                    return;

                case "suggestion":
                    suspect = command[1]
                    weapon = command[2]
                    room = command[3]
                    disprover, disproveCards = self.game_processor_instance.handle_suggestion(self.game_processor_instance.get_current_player(), suspect, weapon, room)

                    # TODO: cannot-disprove popup, unhide for other players
                    # this is incorrect: need to send this json data to the disprove player, not current player
                    # but also the cannot-disprove info to other players
                    return await self.send(json.dumps({
                        "command": "disprove-select",
                        "disprover": disprover.__str__(),
                        "disproveCards": disproveCards
                    }))

                case "disproveReceived":
                    disprover = command[1]
                    disproveCard = command[2]
                    # TODO: handle disprove simultaneously showing cannot-disprove to relevant users and disprove-select
                    self.game_processor_instance.handle_disprove(disprover, disproveCard)  # TODO: need to implement this method
                    self.game_processor_instance.end_turn()

                    return;

                case "validMoves":    # show valid moves
                    possibleSpaces = self.game_processor_instance.get_current_player().get_valid_moves()
                    stringPossibleSpaces = []
                    for sp in possibleSpaces:
                        stringPossibleSpaces.append(sp.__str__())

                    return await self.send(json.dumps({
                        "command": "show-valid-moves",
                        "possibleDestinations": stringPossibleSpaces
                    }))

                case "actualMove":  # actual movement
                    dest = command[1]
                    self.game_processor_instance.move_player(self.game_processor_instance.get_current_player(), self.game_processor_instance.get_space_by_name(dest))
             
                # unknown case
                case _:
                    await self.send(
                        json.dumps(
                            {"status": "error", "message": f"There is no {c} commmand."}
                        )
                    )

        except Exception as e:
            print(f"Error processing message: {e}")
            await self.send(
                json.dumps({"status": "error", "message": "Invalid request format."})
            )

    async def notify(self, event: dict) -> None:
        """
        Send a notification message to the WebSocket client.

        This method is called when a notification event occurs. It sends the message
        contained in the event to the connected WebSocket client.

        Args:
            event (dict): The event dictionary containing the notification message.
        """
        try:
            message = event["message"]  # Extract the message from the event
            await self.send(
                text_data=json.dumps({"message": message})
            )  # Send the notification message to WebSocket
        except KeyError:
            print("Notification event does not contain 'message' key.")
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error while sending notification: {e}")
