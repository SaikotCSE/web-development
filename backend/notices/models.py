# backend/notices/models.py
from django.db import models

CATEGORY_CHOICES = [
    ("General", "General"),
    ("Exam", "Exam"),
    ("Maintenance", "Maintenance"),
    ("Event", "Event"),
    ("Emergency", "Emergency"),
]

class Notice(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default="General")
    author = models.CharField(max_length=120, default="Admin")

    # NEW fields
    pinned = models.BooleanField(default=False)
    attachment_url = models.URLField(null=True, blank=True)

    # Map your existing column `expires_on` to the field name `expires_at`
    # so we don't lose data or need to rename the column in MySQL.
    expires_at = models.DateField(null=True, blank=True, db_column="expires_on")

    # You already have created_at — keep the same column name
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # NEW

    class Meta:
        ordering = ["-pinned", "-created_at"]  # same as your queryset
        db_table = "notices_notice"  # leave default if you didn't change it earlier

    def __str__(self):
        return self.title
