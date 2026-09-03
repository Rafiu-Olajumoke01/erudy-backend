from rest_framework import viewsets, permissions
from .models import Certificate
from .serializers import CertificateSerializer
from accounts.models import User


class IsPlatformOwnerOrSchoolAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [User.Role.PLATFORM_OWNER, User.Role.SCHOOL_ADMIN]
        )


class CertificateViewSet(viewsets.ModelViewSet):
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Certificate.objects.all()
        if user.role == User.Role.STUDENT:
            return Certificate.objects.filter(student=user)
        return Certificate.objects.filter(school=user.school)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPlatformOwnerOrSchoolAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        student = serializer.validated_data['student']
        # Since student is OneToOne, re-uploading should replace, not error out
        Certificate.objects.filter(student=student).delete()
        serializer.save(uploaded_by=self.request.user)