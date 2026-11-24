from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Announcement, Message
from .serializers import AnnouncementSerializer, MessageSerializer
from accounts.models import User
from applications.models import Application
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
            return Announcement.objects.select_related('school', 'posted_by')

        qs = Announcement.objects.select_related('school', 'posted_by').filter(school=user.school)
        if user.role == User.Role.STUDENT:
            return qs.filter(audience__in=['all', 'students'])
        if user.role == User.Role.TUTOR:
            return qs.filter(audience__in=['all', 'tutors'])
        if user.role == User.Role.PARENT:
            return qs.filter(audience__in=['all', 'parents'])
        if user.role in [User.Role.BURSAR, User.Role.REGISTRAR]:
            return qs.filter(audience='all')
        return qs

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

    def perform_update(self, serializer):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            serializer.save()
        else:
            serializer.save(school=user.school)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(Q(sender=user) | Q(recipient=user))

    def perform_create(self, serializer):
        user = self.request.user
        recipient = serializer.validated_data["recipient"]

        if user.role == User.Role.PLATFORM_OWNER:
            serializer.save(sender=user)
            return

        if recipient.school_id != user.school_id:
            raise PermissionDenied("You cannot message this user.")

        if user.role == User.Role.PARENT:
            if recipient.role == User.Role.TUTOR:
                allowed = Application.objects.filter(
                    student__parent_links__parent=user,
                    cohort__tutor=recipient,
                ).exists()
            else:
                allowed = recipient.role == User.Role.SCHOOL_ADMIN
            if not allowed:
                raise PermissionDenied("Parents can only message the admin or their child's tutors.")

        if recipient.role == User.Role.PARENT:
            if user.role == User.Role.TUTOR:
                allowed = Application.objects.filter(
                    student__parent_links__parent=recipient,
                    cohort__tutor=user,
                ).exists()
            else:
                allowed = user.role in [
                    User.Role.SCHOOL_ADMIN,
                    User.Role.BURSAR,
                    User.Role.REGISTRAR,
                ]
            if not allowed:
                raise PermissionDenied("You cannot message this parent.")

        serializer.save(school=user.school, sender=user)