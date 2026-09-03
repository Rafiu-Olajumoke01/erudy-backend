from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = router.urls