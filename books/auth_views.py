from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    """
    Handles user registration.

    This endpoint allows users to create a new account by providing a
    username and password. It checks for duplicate usernames and
    validates the presence of required fields.

    Args:
        request (Request): The HTTP request object containing user data.

    Returns:
        Response:
            - 201 Created: If the user is successfully registered.
            - 400 Bad Request: If the username is already taken or
              if required fields are missing.
    """
    # Retrieve username and password from the request data
    username = request.data.get("username")
    password = request.data.get("password")

    # Validate presence of both username and password
    if not username or not password:
        return Response(
            {"error": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if the username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "The username is already taken. Please choose a new one."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Create a new user
    try:
        User.objects.create_user(username=username, password=password)
    except Exception as e:
        return Response(
            {"error": f"An error occurred while creating the user: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Return success response
    return Response(
        {"message": "User registered successfully."},
        status=status.HTTP_201_CREATED,
    )
