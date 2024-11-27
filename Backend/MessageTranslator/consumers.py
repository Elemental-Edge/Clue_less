import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
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
