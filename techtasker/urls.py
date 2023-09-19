from django.conf.urls import include
from rest_framework import routers
from django.contrib import admin
from django.urls import path
from techtaskerapi.views import register_user, login_user
from techtaskerapi.views import (
    EmployeeView,
    CategoryView,
    DepartmentView,
    WorkOrderView,
    EmployeeWorkOrderView
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'employees', EmployeeView, 'employee')
router.register(r'categories', CategoryView, 'category')
router.register(r'departments', DepartmentView, 'department')
router.register(r'work_orders', WorkOrderView, 'workorder')
router.register(r'employee_work_orders', EmployeeWorkOrderView, 'employeeworkorder')

work_order_view = WorkOrderView.as_view({'put': 'update_status'})  

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('work_orders/<int:pk>/update_status/', work_order_view, name='update-workorder-status')
]
