from django.conf.urls import include
from rest_framework import routers
from django.contrib import admin
from django.urls import path
from techtaskerapi.views import register_user, login_user
from techtaskerapi.views import EmployeeView, CategoryView, DepartmentView, WorkOrderView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'employees', EmployeeView, 'employee')
router.register(r'categories', CategoryView, 'category')
router.register(r'departments', DepartmentView, 'department')
router.register(r'work_orders', WorkOrderView, 'workorder')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls)
]
