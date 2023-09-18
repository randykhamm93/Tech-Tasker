from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from techtaskerapi.models import Employee

from rest_framework import status

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

        if authenticated_user is not None:
            # Authentication successful
            token = Token.objects.get(user=authenticated_user)

            try:
                employee = Employee.objects.get(user=authenticated_user)
                userEmployeeId = employee.id  # Extract the ID
            except Employee.DoesNotExist:
                userEmployeeId = None

            data = {
                'valid': True,
                'token': token.key,
                'is_staff': authenticated_user.is_staff,
                'userEmployeeId': userEmployeeId,
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            data = {'valid': False, 'message': 'Invalid email or password'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
    # Invalid or missing email/password in the request
    data = {'valid': False, 'message': 'Email and password are required'}
    return Response(data, status=status.HTTP_400_BAD_REQUEST)


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
    start_date = request.data.get('start_date', None)
    role = request.data.get('role', None)
    specialty = request.data.get('specialty', None)
    hourly_wage = request.data.get('hourly_wage', None)
    shift = request.data.get('shift', None)
    phone_number=request.data.get('phone_number', None)
    account_type = request.data.get('account_type', None)

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

        # Determine if the user is a supervisor based on account_type
        is_supervisor = account_type == 'supervisor'

        # Create an associated employee entry
        employee = Employee.objects.create(
            user=new_user,
            specialty=specialty,
            start_date=start_date,
            role=role,
            hourly_wage=hourly_wage,
            shift=shift,
            phone_number=phone_number,
            is_supervisor=is_supervisor
        )

        # Use the REST Framework's token generator on the new user account
        token = Token.objects.create(user=new_user)

        data = {'token': token.key, 'is_staff': new_user.is_staff, 'is_supervisor': is_supervisor}
        return Response(data, status=status.HTTP_201_CREATED)

    return Response({'message': 'You must provide email, password, first_name, last_name'}, status=status.HTTP_400_BAD_REQUEST)
