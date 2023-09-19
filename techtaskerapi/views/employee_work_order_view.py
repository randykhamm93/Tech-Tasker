from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from techtaskerapi.models import EmployeeWorkOrder, Employee, WorkOrder


class EmployeeWorkOrderView(ViewSet):
    """Honey Rae API work orders view"""


    def list(self, request):
        """Handle GET requests to get all work orders

        Returns:
            Response -- JSON serialized list of employee work orders
        """

        user_employee_id = request.auth.user.employee.id

        employee_work_orders = EmployeeWorkOrder.objects.filter(employee=user_employee_id)
        serialized = EmployeeWorkOrderSerializer(employee_work_orders, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'full_name',)


class WorkOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = WorkOrder
        fields = ('id', 'title', 'due_date', 'status',)

class EmployeeWorkOrderSerializer(serializers.ModelSerializer):
    """Serializer for EmployeeWorkOrder model"""

    # Assuming you have serializers for Employee and WorkOrder models

    class Meta:
        model = EmployeeWorkOrder
        fields = ('id', 'employee', 'work_order')    

    employee = EmployeeSerializer()
    work_order = WorkOrderSerializer()
