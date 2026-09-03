from rest_framework.routers import DefaultRouter

from .views import CourseViewSet, CohortViewSet

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'cohorts', CohortViewSet, basename='cohort')

urlpatterns = router.urls