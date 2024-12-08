import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async
import string
from django.apps import apps


class NotificationConsumer(AsyncWebsocketConsumer):
    game_in_progress = False
    number_players = 0
    MAX_PLAYERS = 6
    number_choosing_character = 0
    char_to_channel = {}
    channel_to_char = {}
    VALID_CHARS = {"green", "scarlet", "plum", "mustard", "peacock", "white"}

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
            await self.send(
                json.dumps(
                    {"command": "set-channel-name", "channel": self.channel_name}
                )
            )
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

        # remove from notifications channel
        try:
            await self.channel_layer.group_discard(
                "notifications", self.channel_name
            )  # Leave the notifications group
        except Exception as e:
            # Log the error or handle it appropriately
            print(f"Error while disconnecting from notifications group: {e}")

        # remove from active game channel
        try:
            await self.channel_layer.group_discard(
                "activegame", self.channel_name
            )  # Leave the notifications group
        except Exception as e:
            # Log the error or handle it appropriately
            # Do nothing if this fails (will fail if not to char select yet)
            pass

        # unset character
        try:
            c = self.channel_to_char[self.channel_to_chair]
            del self.char_to_channel[c]
            del self.channel_to_char[self.channel_to_chair]
        except:
            pass  # silence this if someone disconnects before selecting a char

        # TODO: Add logic to update gameProcessor so one less player if someone leaves in a game

    async def receive(self, text_data):
        try:
            # Parse the incoming WebSocket message
            command = text_data.split()
            print(text_data)  # TEST STATEMENT
            c = command[0]
            match c:

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

                            # check max players
                            if self.number_players >= self.MAX_PLAYERS:
                                # too many players
                                return await self.send(
                                    json.dumps(
                                        {
                                            "command": "set-text-and-unhide",
                                            "selector": "#login-popup-error",
                                            "text": "Too many players logged in.",
                                        }
                                    )
                                )

                            # check for game in session
                            if self.game_in_progress:
                                # too many players
                                return await self.send(
                                    json.dumps(
                                        {
                                            "command": "set-text-and-unhide",
                                            "selector": "#login-popup-error",
                                            "text": "Game currently in process.",
                                        }
                                    )
                                )

                            self.number_choosing_character = (
                                self.number_choosing_character + 1
                            )

                            # Broadcast player joining to others
                            await self.sendToGame(
                                {
                                    "command": "player-joined-game",
                                    "number_players_choosing_char": self.number_choosing_character,
                                }
                            )

                            # Add user to gameslobby channel
                            await self.channel_layer.group_add(
                                "activegame",  # Group name
                                self.channel_name,  # The user's unique channel
                            )

                            await self.send(
                                json.dumps(
                                    {
                                        "command": "successful-login",
                                        "username": "TODO: Fix Jamie!!",
                                        "number_players_choosing_char": self.number_choosing_character,
                                        "characters_chosen": list(
                                            self.char_to_channel.keys()
                                        ),
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

                        self.number_choosing_character = (
                            self.number_choosing_character + 1
                        )

                        # Broadcast player joining to others
                        await self.sendToGame(
                            {
                                "command": "player-joined-game",
                                "number_players_choosing_char": self.number_choosing_character,
                            }
                        )

                        # Add user to gameslobby channel
                        await self.channel_layer.group_add(
                            "activegame",  # Group name
                            self.channel_name,  # The user's unique channel
                        )

                        return await self.send(
                            json.dumps(
                                {
                                    "command": "successful-register",
                                    "username": "TODO: Jamie again1",
                                    "number_players_choosing_char": self.number_choosing_character,
                                    "characters_chosen": list(
                                        self.char_to_channel.keys()
                                    ),
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

                # selectCharacter
                case "selectCharacter":
                    # first, validate game has not started
                    if self.game_in_progress:
                        # TODO: force logout
                        return await self.send(
                            json.dumps(
                                {
                                    "command": "unrecoverable-error",
                                    "error": "Tried to select character after game was in progress!",
                                }
                            )
                        )

                    # next, validate char is a real character
                    if command[1] not in self.VALID_CHARS:
                        return await self.send(
                            json.dumps(
                                {"error": f"Invalid character selection: {command[1]}"}
                            )
                        )

                    self.char_to_channel[command[1]] = self.channel_name
                    self.channel_to_char[self.channel_name] = command[1]
                    self.number_choosing_character = self.number_choosing_character - 1

                    # added this part - Jon
                    playerToAdd = command[1]
                    try:
                        self.game_processor_instance.add_player(
                            playerToAdd,
                            555555, #TODO: Jamie self.scope["session"].get("_auth_user_id", None),
                        )
                        # TODO: need to add character info to add_player()
                    except ValueError as e:
                        print(f"Value error message: {e}")
                        await self.send(
                            json.dumps({"status": "error", "message": "Value error."})
                        )
                    # end added this part - Jon

                    # Now we can assume the character is good!  Sweeet!
                    return await self.sendToGame(
                        {
                            "command": "character-selected",
                            "selected_by": self.channel_name,
                            "character": command[1],
                            "number_players_choosing_char": self.number_choosing_character,
                            "characters_chosen": list(self.char_to_channel.keys()),
                        }
                    )

                # show/update dealt cards
                case "showDealtCards":
                    cardsStr = []
                    for (
                        card
                    ) in self.game_processor_instance.get_current_player().get_hand():
                        cardsStr.append(card.__str__())

                    return await self.send(
                        json.dumps({"command": "show-dealt-cards", "cards": cardsStr})
                    )

                # get valid actions list for current player
                case "getValidActions":
                    actions_list = self.game_processor_instance.get_valid_actions()

                    return await self.send(
                        json.dumps(
                            {
                                "command": "show-valid-actions",
                                "actions": actions_list.__str__(),  # TODO: need to implement toString for Actions
                            }
                        )
                    )

                case "accusation":
                    suspect = command[1]
                    weapon = command[2]
                    room = command[3]

                    if (
                        suspect == "undefined"
                        or weapon == "undefined"
                        or room == "undefined"
                    ):
                        await self.send(json.dumps({"command": "invalid-action"}))
                    else:
                        # TODO: Add a check to ensure that requesting user is the current player
                        # i.e. selected_character == self.game_processor_instance.get_current_player()
                        result = self.game_processor_instance.handle_accusation(
                            suspect, weapon, room
                        )

                        # TODO: Anytime the gamestate changes need to broadcast message to clients
                        if result:
                            # also need to enter win game state on back-end in addition to win popup
                            winCards = [suspect, weapon, room]
                            await self.send(
                                json.dumps(
                                    {
                                        "command": "win",
                                        "winner": self.game_processor_instance.get_current_player().__str__(),
                                        "winningCards": winCards,
                                    }
                                )
                            )

                            # TODO: need to send this to all non-winning players
                            return await self.send(json.dumps({"command": "lose"}))
                        else:
                            # also need to eliminate player on backend in addition to lose popup
                            # send eliminated player information
                            return await self.send(
                                json.dumps(
                                    {
                                        "command": "eliminate",
                                        "eliminated": self.game_processor_instance.get_current_player().__str__(),
                                    }
                                )
                            )

                    return

                case "suggestion":
                    suspect = command[1]
                    weapon = command[2]

                    if suspect == "undefined" or weapon == "undefined":
                        await self.send(json.dumps({"command": "invalid-action"}))
                    else:
                        room = (
                            self.game_processor_instance.get_current_player().get_current_location()
                        )
                        disprover, disproveCards = (
                            self.game_processor_instance.handle_suggestion(
                                self.game_processor_instance.get_current_player(),
                                suspect,
                                weapon,
                                room,
                            )
                        )

                        # TODO: cannot-disprove popup, unhide for other players
                        # this is incorrect: need to send this json data to the disprove player, not current player
                        # but also the cannot-disprove info to other players
                        await self.send(
                            json.dumps(
                                {
                                    "command": "disprove-select",
                                    "disprover": disprover.__str__(),
                                    "disproveCards": disproveCards,
                                }
                            )
                        )

                        # now get valid actions
                        actions_list = self.game_processor_instance.get_valid_actions()
                        return await self.send(
                            json.dumps(
                                {
                                    "command": "show-valid-actions",
                                    "actions": actions_list.__str__(),  # TODO: need to implement toString for Actions
                                }
                            )
                        )

                case "disproveReceived":
                    disprover = command[1]
                    disproveCard = command[2]
                    # TODO: handle disprove simultaneously showing cannot-disprove to relevant users and disprove-select
                    self.game_processor_instance.handle_disprove(
                        disprover, disproveCard
                    )  # TODO: need to implement this method

                    self.game_processor_instance.end_turn()
                    # need to broadcast to all the cannot-disprove players and send command to unhide cannot-disprove
                    """
                    return await self.send(json.dumps({
                        "command": "cannot-disprove"
                    }))
                    """

                    return

                case "validMoves":  # show valid moves
                    possibleSpaces = (
                        self.game_processor_instance.get_current_player().get_valid_moves()
                    )
                    stringsPossibleSpaces = []
                    for sp in possibleSpaces:
                        stringsPossibleSpaces.append(sp.__str__())

                    return await self.send(
                        json.dumps(
                            {
                                "command": "show-valid-moves",
                                "possibleDestinations": stringsPossibleSpaces,
                            }
                        )
                    )

                case "actualMove":  # actual movement
                    dest = command[1]
                    destName = self.game_processor_instance.get_space_by_name(dest)
                    self.game_processor_instance.move_player(
                        self.game_processor_instance.get_current_player(), destName
                    )

                    # now get valid actions
                    actions_list = self.game_processor_instance.get_valid_actions()

                    return await self.send(
                        json.dumps(
                            {
                                "command": "show-valid-actions",
                                "actions": actions_list.__str__(),  # TODO: need to implement toString for Actions
                            }
                        )
                    )

                case "joinGame":
                    playerToAdd = command[1]
                    try:
                        self.game_processor_instance.add_player(
                            playerToAdd,
                            55555, # TODO: Jamie self.scope["session"].get("_auth_user_id", None),
                        )
                    except ValueError as e:
                        print(f"Value error message: {e}")
                        await self.send(
                            json.dumps({"status": "error", "message": "Value error."})
                        )

                case "startGame":
                    self.game_processor_instance.start_game()
                    return await self.send(
                        json.dumps({"command": "successful-create-game"})
                    )

                case "endTurn":
                    self.game_processor_instance.end_turn()

                    # TODO: broadcast this to next player's client
                    actions_list = self.game_processor_instance.get_valid_actions()

                    return await self.send(
                        json.dumps(
                            {
                                "command": "show-valid-actions",
                                "actions": actions_list.__str__(),  # TODO: need to implement toString for Actions
                            }
                        )
                    )

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

    async def sendToGame(self, dict):
        dict["type"] = "sendToGameHelper"
        await self.channel_layer.group_send("activegame", dict)

    async def sendToGameHelper(self, d):
        # Send the event data to the WebSocket
        del d["type"]
        await self.send(text_data=json.dumps(d))
