"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from techtaskerapi.models import Employee


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
    

class EmployeeSerializer(serializers.ModelSerializer):
    """JSON serializer for employees"""
    
    # Define the email and phone_number fields directly
    email = serializers.CharField(source='user.email', read_only=True)
    
    
    class Meta:
        model = Employee
        fields = ('id', 'user', 'full_name', 'start_date', 'role', 'specialty', 'hourly_wage', 'shift', 'is_supervisor', 'phone_number', 'email',)
