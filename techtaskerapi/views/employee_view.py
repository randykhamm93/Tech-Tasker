"""View module for handling requests for customer data"""
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from techtaskerapi.models import Employee
from django.contrib.auth.models import User



class EmployeeView(ViewSet):
    """Honey Rae API employees view"""

    def list(self, request):
        """Handle GET requests to get all employees

        Returns:
            Response -- JSON serialized list of employees
        """

        employees = Employee.objects.all()
        serialized = EmployeeSerializer(employees, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single employee

        Returns:
            Response -- JSON serialized employee record
        """ 

        employee = Employee.objects.get(pk=pk)
        serialized = EmployeeSerializer(employee, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        """Handle PUT requests to update a work order

        Returns:
            Response -- JSON serialized representation of the updated work order
        """
        try:
            employee = Employee.objects.get(pk=pk)

            # Update the work order fields
            employee.role = request.data.get("role", employee.role)
            employee.specialty = request.data.get("specialty", employee.specialty)
            employee.hourly_wage = request.data.get("hourly_wage", employee.hourly_wage)
            employee.shift = request.data.get("shift", employee.shift)
            employee.start_date = request.data.get("start_date", employee.start_date)
            employee.phone_number = request.data.get("phone_number", employee.phone_number)
            employee.is_supervisor = request.data.get("is_supervisor", employee.is_supervisor)
            user = employee.user
            user.email = request.data.get("email", user.email)
            user.save()
            employee.save()

            serializer = EmployeeSerializer(employee)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({'message': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a work order

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({'message': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)


class EmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for employees"""

    # Define the email and phone_number fields directly
    user = UserSerializer()
    email = serializers.CharField(source='user.email', read_only=True)
    

    class Meta:
        model = Employee
        fields = ('id', 'user', 'full_name', 'start_date', 'role', 'specialty',
                  'hourly_wage', 'shift', 'is_supervisor', 'phone_number', 'email',)
