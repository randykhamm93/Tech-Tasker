"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from techtaskerapi.models import WorkOrder


class WorkOrderView(ViewSet):
    """Honey Rae API work orders view"""

    def list(self, request):
        """Handle GET requests to get all work orders

        Returns:
            Response -- JSON serialized list of work orders
        """

        work_orders = WorkOrder.objects.all()
        serialized = WorkOrderSerializer(work_orders, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single work order

        Returns:
            Response -- JSON serialized work order record
        """

        work_order = WorkOrder.objects.get(pk=pk)
        serialized = WorkOrderSerializer(work_order, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def create(self, request):
        """Handle POST requests for service tickets

        Returns:
            Response: JSON serialized representation of newly created service ticket
        """
        new_work_order = WorkOrder()
        new_work_order.title = request.data.get('title', '')  # Set the title field
        new_work_order.description = request.data['description']
        new_work_order.critical = request.data.get('critical', False)  # Set the critical field, defaulting to False
        new_work_order.status = request.data.get('status', WorkOrder.NOT_STARTED)  # Set the status field, defaulting to 'Not Started'
        new_work_order.due_date = request.data.get('due_date', '')  # Set the due_date field
        new_work_order.created_by_user = request.user  # Set the created_by_user field
        new_work_order.department_id = request.data.get('department', '')  # Set the department field
        new_work_order.category_id = request.data.get('category', '')  # Set the category field

        new_work_order.save()

        serialized = WorkOrderSerializer(new_work_order, many=False)

        return Response(serialized.data, status=status.HTTP_201_CREATED)


class WorkOrderSerializer(serializers.ModelSerializer):
    """JSON serializer for work orders"""
    class Meta:
        model = WorkOrder
        fields = ('id', 'title', 'description', 'critical', 'status', 'due_date', 'created_by_user', 'department', 'category',)
