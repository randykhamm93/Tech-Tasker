from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from techtaskerapi.models import WorkOrder, Category, Department, Employee

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
        """Handle GET requests for a single work order

        Returns:
            Response -- JSON serialized work order record
        """

        try:
            work_order = WorkOrder.objects.get(pk=pk)
            serialized = WorkOrderSerializer(work_order, context={'request': request})
            return Response(serialized.data, status=status.HTTP_200_OK)
        except WorkOrder.DoesNotExist:
            return Response({'message': 'Work Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        """Handle POST requests to create a new work order

        Returns:
            Response -- JSON serialized representation of the newly created work order
        """
       
        try:
            created_by_user = request.auth.user
            assigned_to_ids = request.data.get('assigned_to')  
            category = Category.objects.get(pk=request.data['category'])
            department = Department.objects.get(pk=request.data['department'])
            critical = request.data.get('critical', False)

            work_order = WorkOrder.objects.create(
                title=request.data['title'],
                description=request.data['description'],
                category=category,
                due_date=request.data['due_date'],
                created_by_user=created_by_user,
                status=request.data['status'],
                department=department,
                critical=critical
            )

            for employee_id in assigned_to_ids:
                assigned_employee = Employee.objects.get(id=employee_id)
                work_order.assigned_to.add(assigned_employee)

            serializer = WorkOrderSerializer(work_order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e_msg:
            return Response({'message': str(e_msg)}, status=status.HTTP_400_BAD_REQUEST)

    
    def update(self, request, pk=None):
        """Handle PUT requests to update a work order

        Returns:
            Response -- JSON serialized representation of the updated work order
        """
        try:
            work_order = WorkOrder.objects.get(pk=pk)

            # Update the work order fields
            work_order.title = request.data.get("title", work_order.title)
            work_order.description = request.data.get("description", work_order.description)
            work_order.critical = request.data.get("critical", work_order.critical)
            work_order.status = request.data.get("status", work_order.status)
            work_order.due_date = request.data.get("due_date", work_order.due_date)
            work_order.category = Category.objects.get(pk=request.data.get("category", work_order.category_id))
            work_order.department = Department.objects.get(pk=request.data.get("department", work_order.department_id))

            assigned_to_ids = request.data.get('assigned_to', [])
            work_order.assigned_to.set(assigned_to_ids)

            work_order.save()

            serializer = WorkOrderSerializer(work_order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except WorkOrder.DoesNotExist:
            return Response({'message': 'Work Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        """Handle DELETE requests to delete a work order

        Returns:
            Response -- Empty body with 204 status code
        """
        try:
            work_order = WorkOrder.objects.get(pk=pk)
            work_order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WorkOrder.DoesNotExist:
            return Response({'message': 'Work Order not found'}, status=status.HTTP_404_NOT_FOUND)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', )

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('id', 'full_name', )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', )

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name', )

class WorkOrderSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    department = DepartmentSerializer(many=False)
    created_by_user = UserSerializer(many=False)
    assigned_to = EmployeeSerializer(many=True, read_only=True)  

    class Meta:
        model = WorkOrder
        fields = ('id', 'title', 'description', 'critical', 'status', 'due_date', 'created_by_user', 'department', 'category', 'assigned_to')
