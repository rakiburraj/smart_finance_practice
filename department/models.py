from django.db import models
from django.conf import settings

class Department(models.Model):
    name = models.CharField(max_length=200)
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2)
    finance_head = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='departments')

    def __str__(self):
        return self.name

class DepartmentRep(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE, related_name='rep')

class DepartmentTransaction(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='transactions')
    added_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    file_upload = models.FileField(upload_to='evidence/', blank=True, null=True)

    class Meta:
        ordering = ['-date']