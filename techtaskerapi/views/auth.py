from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from techtaskerapi.models import Employee

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    email = request.data.get('email', None)
    password = request.data.get('password', None)

    if email is not None and password is not None:
        # Use the built-in authenticate method to verify
        # authenticate returns the user object or None if no user is found
        authenticated_user = authenticate(username=email, password=password)

        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)

            data = {
                'valid': True,
                'token': token.key,
                'is_staff': authenticated_user.is_staff
            }
            return Response(data)
    
    # Bad login details were provided. So we can't log the user in.
    data = {'valid': False}
    return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new user for authentication

    Method arguments:
      request -- The full HTTP request object
    '''
    email = request.data.get('email', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    password = request.data.get('password', None)
    account_type = request.data.get('account_type', None)  # Add account_type field
    
    if email is not None and first_name is not None and last_name is not None and password is not None:
        try:
            # Create a new user by invoking the `create_user` helper method
            # on Django's built-in User model
            new_user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
        except IntegrityError:
            return Response(
                {'message': 'An account with that email address already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=new_user)
        
        is_supervisor = False  # Default to not being a supervisor
        if account_type == 'supervisor':
            # If the account type is 'supervisor', set is_supervisor to True
            is_supervisor = True
            # You can add supervisor-specific logic here if needed
        
        # Create an employee entry if it's an employee account
        if not is_supervisor:
            employee = Employee.objects.create(user=new_user, specialty='Default Specialty')  # Modify specialty as needed
        
        data = {'token': token.key, 'is_staff': new_user.is_staff, 'is_supervisor': is_supervisor}
        return Response(data, status=status.HTTP_201_CREATED)

    return Response({'message': 'You must provide email, password, first_name, last_name, and account_type'}, status=status.HTTP_400_BAD_REQUEST)

