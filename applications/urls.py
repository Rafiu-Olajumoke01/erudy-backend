from django.urls import path
from .views import ApplicationCreateView, ApplicationListView, ApplicationDetailView,  ConvertApplicationToStudentView

urlpatterns = [
    path('applications/apply/', ApplicationCreateView.as_view(), name='application-create'),
    path('applications/', ApplicationListView.as_view(), name='application-list'),
    path('applications/<int:pk>/', ApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:pk>/convert-to-student/', ConvertApplicationToStudentView.as_view(), name='application-convert'),
]