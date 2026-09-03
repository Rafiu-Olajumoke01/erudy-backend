from rest_framework.routers import DefaultRouter
from .views import (
    ClassSessionViewSet,
    ClassNoteViewSet,
    AssignmentViewSet,
    AssignmentSubmissionViewSet,
    CapstoneGuidelineViewSet,
)

router = DefaultRouter()
router.register(r'class-sessions', ClassSessionViewSet, basename='class-session')
router.register(r'class-notes', ClassNoteViewSet, basename='class-note')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'assignment-submissions', AssignmentSubmissionViewSet, basename='assignment-submission')
router.register(r'capstone-guidelines', CapstoneGuidelineViewSet, basename='capstone-guideline')

urlpatterns = router.urls