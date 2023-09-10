"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from techtaskerapi.models import Department


class DepartmentView(ViewSet):
    """Honey Rae API departments view"""

    def list(self, request):
        """Handle GET requests to get all departments

        Returns:
            Response -- JSON serialized list of departments
        """

        departments = Department.objects.all()
        serialized = DepartmentSerializer(departments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single department

        Returns:
            Response -- JSON serialized department record
        """

        department = Department.objects.get(pk=pk)
        serialized = DepartmentSerializer(department, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class DepartmentSerializer(serializers.ModelSerializer):
    """JSON serializer for departments"""
    class Meta:
        model = Department
        fields = ('id', 'name', 'description',)
