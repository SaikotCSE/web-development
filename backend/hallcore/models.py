
from django.db import models

class Application(models.Model):
    GENDER_CHOICES = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other"),
    ]

    full_name = models.CharField(max_length=150)
    student_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    session = models.CharField(max_length=50)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    mobile = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    payment_slip_no = models.CharField(max_length=100, unique=True)

    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Approved", "Approved"), ("Rejected", "Rejected")],
        default="Pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.student_id}) - {self.status}"