# backend/users/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Student

User = get_user_model()

# -----------------------------
# User registration / base serializer
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, min_length=6)
    full_name = serializers.CharField(required=True)
    role = serializers.CharField(required=False, default="student")

    class Meta:
        model = User
        # Only include fields we explicitly accept from the client
        fields = ["email", "password", "full_name", "role"]

    def validate_email(self, value: str):
        value = (value or "").strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        """
        Create user with:
        - email lowercased
        - username = email
        - hashed password
        - role defaulted to 'student' if not provided
        """
        email = validated_data["email"].lower()
        password = validated_data["password"]
        full_name = validated_data.get("full_name", "")
        role = validated_data.get("role", "student")

        user = User(
            email=email,
            username=email,   # Use email as username
            full_name=full_name,
            role=role,
            is_active=True,
        )
        user.set_password(password)
        user.save()
        return user


# -----------------------------
# Student profile serializer
# -----------------------------
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        # 'user' is NOT required in fields because we pass it in views via save(user=request.user)
        fields = [
            "student_id",
            "department",
            "session",
            "room_no",
            "dob",
            "gender",
            "blood_group",
            "father_name",
            "mother_name",
            "mobile_number",
            "emergency_number",
            "address",
            "photo_url",
        ]

    def validate_room_no(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Room number must be positive.")
        return value


# -----------------------------
# SimpleJWT: email OR username login
# -----------------------------
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Accepts either:
      { "email": "...", "password": "..." }  OR
      { "username": "...", "password": "..." }
    """
    def validate(self, attrs):
        # SimpleJWT puts identifier in "username"
        identifier = attrs.get("username")
        email = self.initial_data.get("email")

        # If 'email' provided, resolve to actual username of that user
        if email:
            try:
                user = User.objects.get(email__iexact=email)
                attrs["username"] = user.get_username()
            except User.DoesNotExist:
                pass
        # Or if the provided identifier looks like an email, resolve it
        elif identifier and "@" in identifier:
            try:
                user = User.objects.get(email__iexact=identifier)
                attrs["username"] = user.get_username()
            except User.DoesNotExist:
                pass

        return super().validate(attrs)
