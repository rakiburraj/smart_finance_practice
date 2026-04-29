from django.core.management.base import BaseCommand
from django.db.models import Sum
from department.models import Department, DepartmentTransaction
from budget.models import MonthlyBudgetHistory
from datetime import date

class Command(BaseCommand):
    help = 'Run monthly budget carry-over for all departments'

    def handle(self, *args, **kwargs):
        today = date.today()
        # Run for LAST month
        if today.month == 1:
            yr, mo = today.year - 1, 12
        else:
            yr, mo = today.year, today.month - 1

        departments = Department.objects.all()

        for dept in departments:
            txns = DepartmentTransaction.objects.filter(
                department=dept, date__year=yr, date__month=mo
            )
            total_expense = float(txns.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0)
            total_income  = float(txns.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0)
            allocated     = float(dept.monthly_budget)
            saved         = max(allocated - total_expense, 0)
            carry         = saved  # leftover goes to next month

            # Save history
            MonthlyBudgetHistory.objects.update_or_create(
                department=dept, year=yr, month=mo,
                defaults={
                    'allocated':     allocated,
                    'total_expense': total_expense,
                    'total_income':  total_income,
                    'saved':         saved,
                    'carried_over':  carry,
                }
            )

            # Add carry-over to next month
            dept.carried_over = carry
            dept.save()

            self.stdout.write(f'✓ {dept.name} — saved ৳{saved}, carried over ৳{carry}')

        self.stdout.write(self.style.SUCCESS('Month carry-over done!'))