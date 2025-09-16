from django.db import models
from students.models import Student
from admin_panel.models import AdminProfile


class SeatApplication(models.Model):
    application_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fathers_occupation = models.CharField(max_length=255, blank=True, null=True)
    mothers_occupation = models.CharField(max_length=255, blank=True, null=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    year_semester = models.CharField(max_length=50, blank=True, null=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    admin = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='approved_seat_applications')
    
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Seat Application {self.application_id} by {self.student.full_name}"


class SwapRequest(models.Model):
    request_id = models.AutoField(primary_key=True)
    requester = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='swap_requests')
    target = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='swap_targets')
    reason = models.TextField(blank=True, null=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    admin = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='approved_swap_requests')
    
    requested_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Swap Request {self.request_id} from {self.requester.full_name} to {self.target.full_name}"


class Cancellation(models.Model):
    cancellation_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    reason = models.CharField(max_length=100)
    custom_reason = models.TextField(blank=True, null=True)
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    admin = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='approved_cancellations')
    
    document_url = models.CharField(max_length=255, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Cancellation {self.cancellation_id} by {self.student.full_name}"
