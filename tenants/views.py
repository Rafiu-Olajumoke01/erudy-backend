from rest_framework import viewsets, permissions, generics
from accounts.models import User
from cohorts.models import Course
from .models import School
from .serializers import SchoolSerializer, PublicSchoolSerializer, PublicCourseSerializer

class IsPlatformOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.PLATFORM_OWNER


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsPlatformOwner]


class PublicSchoolDetailView(generics.RetrieveAPIView):
    queryset = School.objects.filter(is_active=True)
    serializer_class = PublicSchoolSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []
    lookup_field = 'slug'


class PublicSchoolCourseListView(generics.ListAPIView):
    """Public: list the active courses of one active school, found by its slug."""
    serializer_class = PublicCourseSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get_queryset(self):
        return Course.objects.filter(
            school__slug=self.kwargs['slug'],
            school__is_active=True,
            is_active=True,
        )