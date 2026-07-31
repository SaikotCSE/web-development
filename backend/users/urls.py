from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_date
import json

from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token

from .models import User, Student


# -----------------------------
# Helpers
# -----------------------------

def _json(request):
    try:
        return json.loads(request.body or b"{}")
    except Exception:
        return {}

def _auth_user_from_token(request):
    """
    Returns (user or None, error_json or None)
    Reads header: Authorization: Token <token>
    """
    auth = request.headers.get("Authorization", "")
    prefix = "Token "
    if not auth.startswith(prefix):
        return None, JsonResponse({"error": "Missing or invalid Authorization header"}, status=401)
    token_value = auth[len(prefix):].strip()
    try:
        token = Token.objects.select_related("user").get(key=token_value)
        return token.user, None
    except Token.DoesNotExist:
        return None, JsonResponse({"error": "Invalid token"}, status=401)


# -----------------------------
# Endpoints
# -----------------------------

@csrf_exempt
@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    POST: {full_name, student_id, department, email, password, role}
    Creates User (username=email), returns token + user JSON.
    GET: sanity JSON
    """
    if request.method == "GET":
        return JsonResponse({"detail": "Registration endpoint OK. Use POST."})

    data = _json(request)

    email = (data.get("email") or "").strip().lower()
    password = (data.get("password") or "").strip()
    full_name = (data.get("full_name") or "").strip()
    role = (data.get("role") or "student").strip()

    if not email:
        return JsonResponse({"error": "Email is required"}, status=400)
    if not password:
        return JsonResponse({"error": "Password is required"}, status=400)
    if not full_name:
        return JsonResponse({"error": "Full name is required"}, status=400)

    if User.objects.filter(email__iexact=email).exists():
        return JsonResponse({"error": "User with this email already exists"}, status=400)

    # Create user
    user = User(
        email=email,
        username=email,             # email as username
        full_name=full_name,
        role=role,
        is_active=True,
        is_verified=False,
    )
    user.set_password(password)
    # Optional fields (won't error if your model doesn't have them)
    if hasattr(user, "student_id"):
        user.student_id = data.get("student_id", "")
    if hasattr(user, "department"):
        user.department = data.get("department", "")
    user.save()

    # Create auth token
    token, _ = Token.objects.get_or_create(user=user)

    # Don't create Student record here - let them complete profile manually

    return JsonResponse({
        "message": "User registered successfully",
        "token": token.key,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": getattr(user, "full_name", ""),
            "student_id": getattr(user, "student_id", ""),
            "department": getattr(user, "department", ""),
            "role": getattr(user, "role", "student"),
            "is_verified": getattr(user, "is_verified", True),
        }
    }, status=201)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    POST: {email, password} -> returns token + user JSON
    GET: sanity JSON
    """
    if request.method == "GET":
        return JsonResponse({"detail": "Login endpoint OK. Use POST."})

    data = _json(request)
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return JsonResponse({"error": "Email and password are required"}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    if not user.check_password(password):
        return JsonResponse({"error": "Invalid credentials"}, status=401)

    token, _ = Token.objects.get_or_create(user=user)

    student = Student.objects.filter(user=user).first()
    student_data = None
    if student:
        student_data = {
            "student_id": student.student_id,
            "department": student.department,
            "session": student.session,
            "room_no": student.room_no,
            "photo_url": student.photo_url.url if getattr(student, "photo_url", None) else None,
        }

    return JsonResponse({
        "token": token.key,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": getattr(user, "full_name", ""),
            "student_id": getattr(user, "student_id", ""),
            "department": getattr(user, "department", ""),
            "role": getattr(user, "role", "student"),
            "is_verified": getattr(user, "is_verified", True),
        },
        "student": student_data,
    })


@csrf_exempt
@require_http_methods(["GET"])
def profile_view(request):
    """
    GET current user's profile (requires Authorization: Token <key>)
    """
    user, err = _auth_user_from_token(request)
    if err:
        return err

    student = Student.objects.filter(user=user).first()
    return JsonResponse({
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": getattr(user, "full_name", ""),
            "role": getattr(user, "role", "student"),
            "is_verified": getattr(user, "is_verified", True),
        },
        "student": {
            "student_id": getattr(student, "student_id", ""),
            "department": getattr(student, "department", ""),
            "session": getattr(student, "session", ""),
            "room_no": getattr(student, "room_no", 0),
            "gender": getattr(student, "gender", ""),
            "blood_group": getattr(student, "blood_group", ""),
            "father_name": getattr(student, "father_name", ""),
            "mother_name": getattr(student, "mother_name", ""),
            "mobile_number": getattr(student, "mobile_number", ""),
            "emergency_number": getattr(student, "emergency_number", ""),
            "address": getattr(student, "address", ""),
            "dob": student.dob.isoformat() if getattr(student, "dob", None) else None,
            "photo_url": student.photo_url.url if getattr(student, "photo_url", None) else None,
        } if student else None
    })


# This function is now handled in views.py - removed duplicate
# complete_profile_view is imported from views.py


@csrf_exempt
@require_http_methods(["POST"])
def upload_profile_picture_view(request):
    # Placeholder; implement real file handling later
    return JsonResponse({
        "message": "Profile picture upload endpoint working (placeholder)"
    })


# -----------------------------
# URL patterns (with aliases)
# -----------------------------
# backend/users/urls.py
from django.urls import path
from .views import (
    simple_test_view,
    register_view,
    login_view,
    profile_view,
    complete_profile_view,
    update_profile_view,
    logout_view,
)

urlpatterns = [
    path("auth/register/", register_view, name="users-register"),
    path("auth/login/",    login_view,    name="users-login"),
    path("auth/profile/",  profile_view,  name="users-profile"),
    path("auth/complete-profile/", complete_profile_view, name="users-complete-profile"),
    path("auth/profile/update/", update_profile_view, name="users-profile-update"),
    path("auth/logout/", logout_view, name="users-logout"),

    # simple ping
    path("test/", simple_test_view, name="users-test"),
]

