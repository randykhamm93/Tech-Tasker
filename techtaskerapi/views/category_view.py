"""View module for handling requests for customer data"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from techtaskerapi.models import Category


class CategoryView(ViewSet):
    """Honey Rae API categories view"""

    def list(self, request):
        """Handle GET requests to get all categories

        Returns:
            Response -- JSON serialized list of categories
        """

        categories = Category.objects.all()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized category record
        """

        category = Category.objects.get(pk=pk)
        serialized = CategorySerializer(category, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""
    class Meta:
        model = Category
        fields = ('id', 'name',)
