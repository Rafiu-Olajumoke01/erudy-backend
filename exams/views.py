from rest_framework import viewsets, permissions
from .models import Exam
from .serializers import ExamSerializer
from accounts.models import User


class IsPlatformOwnerOrSchoolAdminOrTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [User.Role.PLATFORM_OWNER, User.Role.SCHOOL_ADMIN, User.Role.TUTOR]
        )


class ExamViewSet(viewsets.ModelViewSet):
    serializer_class = ExamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Exam.objects.all()
        return Exam.objects.filter(school=user.school)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPlatformOwnerOrSchoolAdminOrTutor()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            serializer.save(created_by=user)
        else:
            serializer.save(school=user.school, created_by=user)