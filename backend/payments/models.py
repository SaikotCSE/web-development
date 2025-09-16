from django.db import models
from students.models import Student
from admin_panel.models import AdminProfile


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    admin = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='processed_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=100, blank=True, null=True)
    payment_date = models.DateField(blank=True, null=True)
    receipt_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment {self.payment_id} of {self.amount} by {self.student.full_name}"
