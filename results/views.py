from rest_framework import viewsets, permissions
from .models import Result
from .serializers import ResultSerializer
from accounts.models import User


class IsPlatformOwnerOrSchoolAdminOrTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [User.Role.PLATFORM_OWNER, User.Role.SCHOOL_ADMIN, User.Role.TUTOR]
        )


class ResultViewSet(viewsets.ModelViewSet):
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Result.objects.all()
        if user.role == User.Role.STUDENT:
            return Result.objects.filter(application__student=user)
        return Result.objects.filter(exam__school=user.school)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPlatformOwnerOrSchoolAdminOrTutor()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(graded_by=self.request.user)