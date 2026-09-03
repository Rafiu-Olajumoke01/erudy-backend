from rest_framework import viewsets, permissions
from .models import ClassSession, ClassNote, Assignment, AssignmentSubmission, CapstoneGuideline
from .serializers import (
    ClassSessionSerializer, ClassNoteSerializer, AssignmentSerializer,
    AssignmentSubmissionSerializer, CapstoneGuidelineSerializer,
)
from accounts.models import User


class IsPlatformOwnerOrSchoolAdminOrTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [User.Role.PLATFORM_OWNER, User.Role.SCHOOL_ADMIN, User.Role.TUTOR]
        )


class SchoolScopedMixin:
    """Shared queryset scoping: Platform Owner sees all, everyone else sees only their own school's records."""

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return self.queryset.all()
        return self.queryset.filter(school=user.school)


class ClassSessionViewSet(SchoolScopedMixin, viewsets.ModelViewSet):
    queryset = ClassSession.objects.all()
    serializer_class = ClassSessionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPlatformOwnerOrSchoolAdminOrTutor()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            serializer.save()
        else:
            serializer.save(school=user.school)


class ClassNoteViewSet(SchoolScopedMixin, viewsets.ModelViewSet):
    queryset = ClassNote.objects.all()
    serializer_class = ClassNoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPlatformOwnerOrSchoolAdminOrTutor()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            serializer.save(uploaded_by=user)
        else:
            serializer.save(school=user.school, uploaded_by=user)


class AssignmentViewSet(SchoolScopedMixin, viewsets.ModelViewSet):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class CapstoneGuidelineViewSet(SchoolScopedMixin, viewsets.ModelViewSet):
    queryset = CapstoneGuideline.objects.all()
    serializer_class = CapstoneGuidelineSerializer
    permission_classes = [permissions.IsAuthenticated]

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


class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    """Students submit their own work; Tutors/Admin can view all submissions for their school's assignments."""
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return AssignmentSubmission.objects.all()
        if user.role == User.Role.STUDENT:
            return AssignmentSubmission.objects.filter(student=user)
        # School Admin / Tutor — see submissions for assignments in their own school
        return AssignmentSubmission.objects.filter(assignment__school=user.school)

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)