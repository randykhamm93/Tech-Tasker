from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True, auto_now=False, auto_now_add=False)
    specialty = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
    hourly_wage = models.DecimalField( max_digits=5, decimal_places=2)
    shift = models.CharField(max_length=15)
    is_supervisor = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15)
    
    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def formatted_hourly_wage(self):
        return f'${self.hourly_wage:.2f}'
