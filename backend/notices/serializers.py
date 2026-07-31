from rest_framework import serializers
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = [
            "id",
            "title",
            "body",
            "category",
            "author",
            "pinned",
            "attachment_url",  # must exist on the model
            "expires_at",      # must exist on the model (DateTimeField null=True, blank=True)
            "created_at",
            "updated_at",
        ]
        read_only_fields = ("id", "created_at", "updated_at")
