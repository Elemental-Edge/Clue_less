from django.views import View
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.shortcuts import render

class GameView(View):
        def post(self, request):
            # Logic to start a new game or join an existing one
            pass

        def get(self, request, game_id):
            # Logic to retrieve game state
              pass

class CreateGameView(View):
    """
    View for handling a player to create a game.

    This view allows users to create game lobbies.

    Methods:
        post(request): Handles creating game lobbies via POST request.
    """

    def post(self, request) -> JsonResponse:
        """
        Handles creating game lobbies via POST request.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating success or failure.
        """

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)

class JoinGameView(View):
    """
    View for handling player joining games.

    This view allows users to join game lobbies.

    Methods:
        post(request): Handles joining game lobbies via POST request.
    """

    def post(self, request) -> JsonResponse:
        """
        Handles joining game lobbies via POST request.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating success or failure.
        """

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)

class LeaveGameView(View):
    """
    View for handling player leaving a game.

    This view allows users to leave game lobbies.

    Methods:
        post(request): Handles leaving game lobbies via POST request.
    """

    def post(self, request) -> JsonResponse:
        """
        Handles leaving game lobbies via POST request.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating success or failure.
        """

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)

class StartGameView(View):
    """
    View for handling player starting a game.

    This view allows users to start games.

    Methods:
        post(request): Handles start games via POST request.
    """

    def post(self, request) -> JsonResponse:
        """
        Handles starting games via POST request.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating success or failure.
        """

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)

class ChooseCharacterView(View):
    """
    View for choosing a character.

    This view allows users to choose character.

    Methods:
        post(request): Handles choosing character via POST request.
    """

    def post(self, request) -> JsonResponse:
        """
        Handles choosing characters via POST request.

        Args:
            request: The HTTP request object.

        Returns:
            JsonResponse: A JSON response indicating success or failure.
        """

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)

class PlayerMoveView(View):

    def post(self, request) -> JsonResponse:

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)

class MakeSuggestionView(View):

    def post(self, request) -> JsonResponse:
        from django.apps import apps

        # myapp/consumers.py
        for i in apps.get_app_configs():
            print(i)

        my_app_config = apps.get_app_config('GameManagement')
        singleton_instance = my_app_config.get_singleton()

        # Now you can use the singleton_instance in your consumer
        singleton_instance.initialize()
        singleton_instance.some_method()

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # Notify all clients of the new login
        channel_layer = get_channel_layer()
        username = request.user.username
        async_to_sync(channel_layer.group_send)(
            "notifications",
            {
                'type': 'notify',
                'message': f" {username} Made a Suggestion.",
            }
        )

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)

class MakeAccusationView(View):

    def post(self, request) -> JsonResponse:

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)

class EndTurnView(View):

    def post(self, request) -> JsonResponse:

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)

class EndGameEarlyRequestView(View):

    def post(self, request) -> JsonResponse:

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)

class EndGameEarlyVoteView(View):

    def post(self, request) -> JsonResponse:

        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB
        # TODO: THIS IS A STUB

        return JsonResponse({'message': 'This feature has not been implemented yet.'}, status=200)