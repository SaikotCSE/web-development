from django.db import models
from admin_panel.models import AdminProfile


class Notice(models.Model):
    notice_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_by = models.ForeignKey(AdminProfile, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='created_notices')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
