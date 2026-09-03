from rest_framework import viewsets, permissions
from .models import Classwork, ClassworkSubmission
from .serializers import ClassworkSerializer, ClassworkSubmissionSerializer
from accounts.models import User


class IsPlatformOwnerOrSchoolAdminOrTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [User.Role.PLATFORM_OWNER, User.Role.SCHOOL_ADMIN, User.Role.TUTOR]
        )


class ClassworkViewSet(viewsets.ModelViewSet):
    serializer_class = ClassworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Classwork.objects.all()
        return Classwork.objects.filter(school=user.school)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPlatformOwnerOrSchoolAdminOrTutor()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            serializer.save(posted_by=user)
        else:
            serializer.save(school=user.school, posted_by=user)


class ClassworkSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = ClassworkSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return ClassworkSubmission.objects.all()
        if user.role == User.Role.STUDENT:
            return ClassworkSubmission.objects.filter(student=user)
        return ClassworkSubmission.objects.filter(classwork__school=user.school)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)