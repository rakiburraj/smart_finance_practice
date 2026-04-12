from django.contrib import admin
from .models import Department, DepartmentRep, DepartmentTransaction

admin.site.register(Department)
admin.site.register(DepartmentRep)
admin.site.register(DepartmentTransaction)