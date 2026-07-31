# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from users.views import EmailOrUsernameTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/users/", include("users.urls")),
    path("api/notices/", include("notices.urls")),
    path("api/", include("hallcore.urls")),

    # JWT login (email OR username)
    path("api/token/", EmailOrUsernameTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
