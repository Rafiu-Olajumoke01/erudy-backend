from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, PublicSchoolDetailView, PublicSchoolCourseListView

router = DefaultRouter()
router.register(r'schools', SchoolViewSet, basename='school')

urlpatterns = [
    path('public/schools/<slug:slug>/', PublicSchoolDetailView.as_view(), name='public-school-detail'),
    path('public/schools/<slug:slug>/courses/', PublicSchoolCourseListView.as_view(), name='public-school-courses'),
] + router.urls