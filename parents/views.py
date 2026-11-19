from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets
from rest_framework.permissions import BasePermission, IsAuthenticated

from .models import ParentStudentLink
from .serializers import ChildSerializer, ParentStudentLinkSerializer

User = get_user_model()


class IsAdminRole(BasePermission):
    """Only Platform Owner and School Admin can manage links."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in (
            'platform_owner',
            'school_admin',
        )


class IsParentRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'parent'


class ParentStudentLinkViewSet(viewsets.ModelViewSet):
    serializer_class = ParentStudentLinkSerializer

    def get_permissions(self):
        # Parents may only read their own links; admins can do everything
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [IsAuthenticated()]
        return [IsAdminRole()]

    def get_queryset(self):
        user = self.request.user
        qs = ParentStudentLink.objects.select_related('parent', 'student')

        if user.role == 'platform_owner':
            return qs
        if user.role == 'school_admin':
            return qs.filter(school=user.school)
        if user.role == 'parent':
            return qs.filter(parent=user)
        return qs.none()

    def perform_create(self, serializer):
        # School always comes from the parent, never from the request
        parent = serializer.validated_data['parent']
        serializer.save(school=parent.school)


class MyChildrenView(generics.ListAPIView):
    """A parent sees only their own children."""

    serializer_class = ChildSerializer
    permission_classes = [IsParentRole]

    def get_queryset(self):
        return User.objects.filter(parent_links__parent=self.request.user)