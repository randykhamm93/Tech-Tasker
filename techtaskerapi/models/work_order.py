from django.db import models
from django.contrib.auth.models import User


class WorkOrder(models.Model):

    NOT_STARTED = 'Not Started'
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (NOT_STARTED, 'Not Started'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    title = models.CharField(max_length=75)
    description = models.TextField()
    critical = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NOT_STARTED,
    )
    due_date = models.DateField()
    created_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey("Department", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    assigned_to = models.ManyToManyField(
        "Employee", through="EmployeeWorkOrder")
