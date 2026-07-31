from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Custom User model
class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=[('student', 'Student'), ('admin', 'Admin')])
    full_name = models.CharField(max_length=255, blank=True)
    student_id = models.CharField(max_length=50, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_verified = models.BooleanField(default=False)

    # Adding related_name to avoid reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Adding related_name to prevent clashes
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Adding related_name to prevent clashes
        blank=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']

    def __str__(self):
        return self.email


# Student Profile model  
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    student_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    session = models.CharField(max_length=100, blank=True)
    room_no = models.IntegerField(default=0)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True)
    blood_group = models.CharField(max_length=5, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ], blank=True)
    father_name = models.CharField(max_length=255, blank=True)
    mother_name = models.CharField(max_length=255, blank=True)
    mobile_number = models.CharField(max_length=20, blank=True)
    emergency_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    photo_url = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def is_profile_complete(self):
        """Check if all required profile fields are filled"""
        required_fields = [
            self.student_id, self.department, self.session, self.dob,
            self.gender, self.mobile_number, self.emergency_number, self.address
        ]
        return all(field for field in required_fields if field not in [None, '', 0])

    def __str__(self):
        return f"{self.user.email} - {self.student_id}"
