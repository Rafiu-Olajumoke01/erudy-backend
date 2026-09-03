from rest_framework.routers import DefaultRouter
from .views import ClassworkViewSet, ClassworkSubmissionViewSet

router = DefaultRouter()
router.register(r'classwork', ClassworkViewSet, basename='classwork')
router.register(r'classwork-submissions', ClassworkSubmissionViewSet, basename='classwork-submission')

urlpatterns = router.urls