# backend/authentication/views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from channels.layers import get_channel_layer


def registerController(data):
    form = UserCreationForm(data)  # Create a form instance with POST data

    if form.is_valid():
        user = form.save()  # Save the new user
        return JsonResponse({'message': 'User created successfully'}, status=201)

    # If the form is not valid display and return errors
    print(f"Errors: {form.errors}")  # Debug message
    return JsonResponse({'errors': form.errors}, status=400)