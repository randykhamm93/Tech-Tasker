from django.conf.urls import include
from rest_framework import routers
from django.contrib import admin
from django.urls import path
from techtaskerapi.views import register_user, login_user
from techtaskerapi.views import EmployeeView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'employees', EmployeeView, 'employee')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls)
]
