from django.db import models

class EmployeeWorkOrder(models.Model):
    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    work_order = models.ForeignKey("WorkOrder", on_delete=models.CASCADE)
