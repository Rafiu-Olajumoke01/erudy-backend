from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Attendance
from .serializers import AttendanceSerializer, BulkAttendanceSerializer
from accounts.models import User
from academics.models import ClassSession
from applications.models import Application


class IsPlatformOwnerOrSchoolAdminOrTutor(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [User.Role.PLATFORM_OWNER, User.Role.SCHOOL_ADMIN, User.Role.TUTOR]
        )


class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Attendance.objects.all()
        if user.role == User.Role.STUDENT:
            return Attendance.objects.filter(application__student=user)
        # School Admin / Tutor — see records for their own school
        return Attendance.objects.filter(session__school=user.school)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsPlatformOwnerOrSchoolAdminOrTutor()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(marked_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(marked_by=self.request.user)


class BulkMarkAttendanceView(APIView):
    """Mark attendance for an entire session's roster in one request."""
    permission_classes = [IsPlatformOwnerOrSchoolAdminOrTutor]

    def post(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        session_id = serializer.validated_data['session']
        entries = serializer.validated_data['entries']

        session = get_object_or_404(ClassSession, pk=session_id)

        user = request.user
        if user.role != User.Role.PLATFORM_OWNER and session.school_id != user.school_id:
            return Response({"detail": "You cannot mark attendance for another school's session."}, status=status.HTTP_403_FORBIDDEN)

        results = []
        errors = []

        for entry in entries:
            application_id = entry['application']
            attendance_status = entry['status']

            try:
                application = Application.objects.get(pk=application_id)
            except Application.DoesNotExist:
                errors.append({"application": application_id, "error": "Application not found."})
                continue

            if application.cohort_id != session.cohort_id:
                errors.append({"application": application_id, "error": "Not enrolled in this session's cohort."})
                continue

            attendance, created = Attendance.objects.update_or_create(
                session=session,
                application=application,
                defaults={'status': attendance_status, 'marked_by': user},
            )
            results.append(AttendanceSerializer(attendance).data)

        return Response({"marked": results, "errors": errors}, status=status.HTTP_201_CREATED)