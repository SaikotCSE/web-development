from django.db import models
from students.models import Student
from admin_panel.models import AdminProfile  # Import your admin model


class Complaint(models.Model):
    complaint_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    admin = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='managed_complaints')
    category = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Complaint {self.complaint_id} by {self.student.full_name} - {self.status}"
