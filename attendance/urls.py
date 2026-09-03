from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AttendanceViewSet, BulkMarkAttendanceView

router = DefaultRouter()
router.register(r'attendance', AttendanceViewSet, basename='attendance')

urlpatterns = [
    path('attendance/bulk-mark/', BulkMarkAttendanceView.as_view(), name='attendance-bulk-mark'),
    path('', include(router.urls)),
]