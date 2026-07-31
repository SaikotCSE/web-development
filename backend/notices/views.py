from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from .models import Notice
from .serializers import NoticeSerializer

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by("-pinned", "-created_at")
    serializer_class = NoticeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return [AllowAny()]
