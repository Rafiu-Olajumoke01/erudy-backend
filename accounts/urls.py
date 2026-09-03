from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import CreateSchoolAdminView, CreateTutorView, UserListView

urlpatterns = [
    path('login/', obtain_auth_token, name='api-login'),
    path('users/create-school-admin/', CreateSchoolAdminView.as_view(), name='create-school-admin'),
    path('users/create-tutor/', CreateTutorView.as_view(), name='create-tutor'),
    path('users/', UserListView.as_view(), name='user-list'),
]