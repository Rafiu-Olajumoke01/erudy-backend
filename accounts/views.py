from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer


class IsPlatformOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.PLATFORM_OWNER


class IsSchoolAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.SCHOOL_ADMIN


class CreateSchoolAdminView(generics.CreateAPIView):
    """Platform Owner creates a School Admin for a specific school."""
    serializer_class = UserSerializer
    permission_classes = [IsPlatformOwner]

    def perform_create(self, serializer):
        serializer.save(role=User.Role.SCHOOL_ADMIN)


class CreateTutorView(generics.CreateAPIView):
    """School Admin creates a Tutor — automatically tied to their own school."""
    serializer_class = UserSerializer
    permission_classes = [IsSchoolAdmin]

    def perform_create(self, serializer):
        serializer.save(role=User.Role.TUTOR, school=self.request.user.school)


class UserListView(generics.ListAPIView):
    """List users — scoped to the requester's own school (except Platform Owner sees all)."""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return User.objects.all()
        return User.objects.filter(school=user.school)