# backend/users/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Student
from .serializers import UserSerializer, StudentSerializer

# JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailOrUsernameTokenObtainPairSerializer  # make sure you added this as we discussed

User = get_user_model()

def _jwt_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)

@api_view(["GET"])
@permission_classes([AllowAny])
def simple_test_view(request):
    return Response({"message": "Simple test working!", "status": "ok"})

@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register a new user.
    Expects: { email, password, full_name, role?, student_id?, department? }
    Returns: { message, access, refresh, user }
    """
    data = request.data.copy()
    serializer = UserSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()

    # Optional extras if your User model has these fields
    for opt_field in ("student_id", "department"):
        if hasattr(user, opt_field) and data.get(opt_field) is not None:
            setattr(user, opt_field, data.get(opt_field))
    user.save()

    # Optional Student profile shell
    if data.get("student_id") or data.get("department"):
        Student.objects.get_or_create(
            user=user,
            defaults={
                "student_id": data.get("student_id", ""),
                "department": data.get("department", ""),
            },
        )

    access, refresh = _jwt_for_user(user)

    return Response(
        {
            "message": "User registered successfully",
            "access": access,
            "refresh": refresh,
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
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Email + password login (JWT).
    Expects: { email, password }
    Returns: { access, refresh, user, student? }
    """
    email = (request.data.get("email") or "").strip().lower()
    password = request.data.get("password") or ""
    if not email or not password:
        return Response({"error": "Email and password are required"}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=401)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=401)

    access, refresh = _jwt_for_user(user)
    student = Student.objects.filter(user=user).first()
    student_data = StudentSerializer(student).data if student else None

    return Response(
        {
            "access": access,
            "refresh": refresh,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": getattr(user, "full_name", ""),
                "role": getattr(user, "role", "student"),
                "is_verified": getattr(user, "is_verified", True),
            },
            "student": student_data,
        },
        status=200,
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Stateless JWT doesn't need server-side logout.
    Optional: add your own token blacklist if enabled.
    """
    return Response({"message": "Logged out (client should discard tokens)."}, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    student = Student.objects.filter(user=user).first()
    return Response(
        {
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": getattr(user, "full_name", ""),
                "role": getattr(user, "role", "student"),
                "is_verified": getattr(user, "is_verified", True),
            },
            "student": StudentSerializer(student).data if student else None,
        },
        status=200,
    )


# First complete_profile_view function removed - using the one below with proper logic


# backend/users/views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Student
from .serializers import UserSerializer, StudentSerializer

# JWT
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailOrUsernameTokenObtainPairSerializer  # ensure you added this in serializers.py

User = get_user_model()

def _jwt_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)

@api_view(["GET"])
@permission_classes([AllowAny])
def simple_test_view(request):
    return Response({"message": "Simple test working!", "status": "ok"})

@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """
    Register user; returns {access, refresh, user}
    """
    data = request.data.copy()
    serializer = UserSerializer(data=data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()

    for opt_field in ("student_id", "department"):
        if hasattr(user, opt_field) and data.get(opt_field) is not None:
            setattr(user, opt_field, data.get(opt_field))
    user.save()

    if data.get("student_id") or data.get("department"):
        Student.objects.get_or_create(
            user=user,
            defaults={
                "student_id": data.get("student_id", ""),
                "department": data.get("department", ""),
            },
        )

    access, refresh = _jwt_for_user(user)

    return Response(
        {
            "message": "User registered successfully",
            "access": access,
            "refresh": refresh,
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
        },
        status=status.HTTP_201_CREATED,
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    """
    Email + password login; returns {access, refresh, user, student?}
    """
    email = (request.data.get("email") or "").strip().lower()
    password = request.data.get("password") or ""
    if not email or not password:
        return Response({"error": "Email and password are required"}, status=400)

    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=401)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=401)

    access, refresh = _jwt_for_user(user)
    student = Student.objects.filter(user=user).first()
    student_data = StudentSerializer(student).data if student else None

    return Response(
        {
            "access": access,
            "refresh": refresh,
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": getattr(user, "full_name", ""),
                "role": getattr(user, "role", "student"),
                "is_verified": getattr(user, "is_verified", True),
            },
            "student": student_data,
        },
        status=200,
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # Stateless JWT: no server action needed
    return Response({"message": "Logged out (discard tokens client-side)."}, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    student = Student.objects.filter(user=user).first()
    return Response(
        {
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "full_name": getattr(user, "full_name", ""),
                "role": getattr(user, "role", "student"),
                "is_verified": getattr(user, "is_verified", True),
            },
            "student": StudentSerializer(student).data if student else None,
        },
        status=200,
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def complete_profile_view(request):
    user = request.user
    student = Student.objects.filter(user=user).first()
    
    # Determine if this is initial profile setup or profile update
    is_initial_setup = not user.is_verified  # New users are not verified yet
    
    # Handle both JSON and multipart form data
    if request.content_type and 'multipart/form-data' in request.content_type:
        # File upload case - use request.POST and request.FILES
        data = dict(request.POST)
        # Convert single-item lists to values (FormData sends arrays)
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 1:
                data[key] = value[0]
        
        # Handle file upload
        if 'photo' in request.FILES:
            data['photo_url'] = request.FILES['photo']
    else:
        # JSON case - use request.data
        data = request.data
    
    if student:
        # Profile exists, update it
        serializer = StudentSerializer(student, data=data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            
            # Set user as verified if this is initial setup
            if is_initial_setup:
                user.is_verified = True
                user.save()
                message = "Profile completed successfully"
            else:
                message = "Profile updated successfully"
            
            return Response(
                {"success": True, "message": message, "student": StudentSerializer(updated).data},
                status=200,
            )
        return Response(serializer.errors, status=400)
    else:
        # Profile doesn't exist, create it
        payload = data.copy()
        payload["user"] = user.id
        serializer = StudentSerializer(data=payload)
        if serializer.is_valid():
            student = serializer.save(user=user)
            
            # Mark user as verified after successful profile creation
            user.is_verified = True
            user.save()
            
            return Response(
                {"success": True, "message": "Profile completed successfully", "student": StudentSerializer(student).data},
                status=200,
            )
        return Response(serializer.errors, status=400)

@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    user = request.user
    student = Student.objects.filter(user=user).first()
    if not student:
        return Response({"error": "Profile not found. Please complete your profile first."}, status=404)

    serializer = StudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        updated = serializer.save()
        return Response(
            {"message": "Profile updated successfully", "student": StudentSerializer(updated).data},
            status=200,
        )
    return Response(serializer.errors, status=400)

class EmailOrUsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailOrUsernameTokenObtainPairSerializer


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    user = request.user
    student = Student.objects.filter(user=user).first()
    if not student:
        return Response({"error": "Profile not found. Please complete your profile first."}, status=404)

    serializer = StudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        updated = serializer.save()
        return Response(
            {"message": "Profile updated successfully", "student": StudentSerializer(updated).data},
            status=200,
        )
    return Response(serializer.errors, status=400)

# Optional: email/username JWT endpoint
class EmailOrUsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailOrUsernameTokenObtainPairSerializer
