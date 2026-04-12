from django.db import models
from django.conf import settings
from department.models import Department

class BudgetRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='budget_requests')
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    justification = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    response_date = models.DateTimeField(blank=True, null=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-request_date']