from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MyChildrenView, ParentStudentLinkViewSet

router = DefaultRouter()
router.register('links', ParentStudentLinkViewSet, basename='parent-link')

urlpatterns = [
    path('my-children/', MyChildrenView.as_view(), name='my-children'),
    path('', include(router.urls)),
]