from rest_framework import generics, permissions
from .models import Application
from .serializers import ApplicationCreateSerializer, ApplicationSerializer
from accounts.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import ConvertToStudentSerializer


class IsPlatformOwnerOrSchoolAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in [User.Role.PLATFORM_OWNER, User.Role.SCHOOL_ADMIN]
        )


class ApplicationCreateView(generics.CreateAPIView):
    """Public endpoint — anyone can apply, no login required."""
    queryset = Application.objects.all()
    serializer_class = ApplicationCreateSerializer
    permission_classes = [permissions.AllowAny]


class ApplicationListView(generics.ListAPIView):
    """School Admin sees only their school's applications; Platform Owner sees all."""
    serializer_class = ApplicationSerializer
    permission_classes = [IsPlatformOwnerOrSchoolAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Application.objects.all()
        return Application.objects.filter(school=user.school)


class ApplicationDetailView(generics.RetrieveUpdateAPIView):
    """View/update a single application — approve/reject, assign student, assign cohort."""
    serializer_class = ApplicationSerializer
    permission_classes = [IsPlatformOwnerOrSchoolAdmin]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.PLATFORM_OWNER:
            return Application.objects.all()
        return Application.objects.filter(school=user.school)

class ConvertApplicationToStudentView(APIView):
    """School Admin/Platform Owner converts a paid, approved application into a real Student account."""
    permission_classes = [IsPlatformOwnerOrSchoolAdmin]

    def post(self, request, pk):
        application = get_object_or_404(Application, pk=pk)

        user = request.user
        if user.role == User.Role.SCHOOL_ADMIN and application.school_id != user.school_id:
            return Response({"detail": "You cannot convert an application from another school."}, status=status.HTTP_403_FORBIDDEN)

        serializer = ConvertToStudentSerializer(data=request.data, context={'application': application})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_201_CREATED)