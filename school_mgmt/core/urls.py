from django.urls import path, include
from rest_framework.routers import DefaultRouter

from core.views import (
    StudentViewSet,SubjectViewSet,ExamCategoryViewSet,ScoreViewSet,ExamViewSet,

)

router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'exam-categories', ExamCategoryViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'scores', ScoreViewSet)

urlpatterns = [
    path('', include(router.urls)),

]