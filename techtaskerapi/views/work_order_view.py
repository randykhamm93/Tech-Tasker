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


class WorkOrderSerializer(serializers.ModelSerializer):
    """JSON serializer for work orders"""
    class Meta:
        model = WorkOrder
        fields = ('id', 'title', 'description', 'critical', 'status', 'due_date', 'created_by_user', 'department', 'category',)
