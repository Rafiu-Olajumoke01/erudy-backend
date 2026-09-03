from rest_framework import viewsets, permissions

from accounts.models import User
from .models import Course, Cohort
from .serializers import CourseSerializer, CohortSerializer


class IsPlatformOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.PLATFORM_OWNER


class IsSchoolAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.SCHOOL_ADMIN


class IsPlatformOwnerOrSchoolAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [
            User.Role.PLATFORM_OWNER,
            User.Role.SCHOOL_ADMIN,
        ]


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPlatformOwnerOrSchoolAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Course.objects.all()
        return Course.objects.filter(school=user.school)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            serializer.save()
        else:
            serializer.save(school=user.school)


class CohortViewSet(viewsets.ModelViewSet):
    serializer_class = CohortSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPlatformOwnerOrSchoolAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Cohort.objects.all()
        if user.role == User.Role.TUTOR:
            return Cohort.objects.filter(tutor=user)
        return Cohort.objects.filter(school=user.school)

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            serializer.save()
        else:
            serializer.save(school=user.school)