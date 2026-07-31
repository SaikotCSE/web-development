from django.urls import path
from .views import ApplicationCreateView, ApplicationListView, ApplicationUpdateStatusView

urlpatterns = [
    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('applications/create/', ApplicationCreateView.as_view(), name='application-create'),
    path('applications/<int:pk>/status/', ApplicationUpdateStatusView.as_view(), name='application-update-status'),
]