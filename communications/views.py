from rest_framework import viewsets, permissions
from .models import Announcement, Message
from .serializers import AnnouncementSerializer, MessageSerializer
from accounts.models import User
from django.db.models import Q


class IsPlatformOwnerOrSchoolAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [User.Role.PLATFORM_OWNER, User.Role.SCHOOL_ADMIN]
        )


class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Announcement.objects.all()

        qs = Announcement.objects.filter(school=user.school)
        if user.role == User.Role.STUDENT:
            return qs.filter(audience__in=['all', 'students'])
        if user.role == User.Role.TUTOR:
            return qs.filter(audience__in=['all', 'tutors'])
        return qs  # School Admin sees everything for their school

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPlatformOwnerOrSchoolAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            serializer.save(posted_by=user)
        else:
            serializer.save(school=user.school, posted_by=user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(recipient=user))

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            serializer.save(sender=user)
        else:
            serializer.save(school=user.school, sender=user)