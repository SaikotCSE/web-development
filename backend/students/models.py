from django.db import models
from core.models import User  # Assuming your User model is in core app


class Student(models.Model):
    student_id = models.IntegerField(primary_key=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    department = models.CharField(max_length=100, blank=True, null=True)
    session = models.CharField(max_length=50, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    
    mobile_number = models.CharField(max_length=20, blank=True, null=True)
    fathers_name = models.CharField(max_length=255, blank=True, null=True)
    mothers_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_number = models.CharField(max_length=20, blank=True, null=True)
    permanent_address = models.TextField(blank=True, null=True)
    photo_url = models.CharField(max_length=255, blank=True, null=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.student_id})"


class StudentRoom(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    room_no = models.IntegerField()
    assigned_on = models.DateField()

    def __str__(self):
        return f"Room {self.room_no} assigned to {self.student.full_name}"
