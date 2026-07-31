from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Application
from .serializers import ApplicationSerializer

# Existing views (keep them)
class ApplicationCreateView(generics.CreateAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class ApplicationListView(generics.ListAPIView):
    queryset = Application.objects.all().order_by("-created_at")
    serializer_class = ApplicationSerializer

# New view to update status (Approve/Reject)
class ApplicationUpdateStatusView(APIView):
    def patch(self, request, pk):
        try:
            app = Application.objects.get(pk=pk)
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

        status_value = request.data.get("status")
        if status_value not in ["Approved", "Rejected"]:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        app.status = status_value
        app.save()
        serializer = ApplicationSerializer(app)
        return Response(serializer.data)