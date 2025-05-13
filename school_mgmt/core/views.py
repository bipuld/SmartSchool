from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from rest_framework.permissions import AllowAny  
from drf_spectacular.utils import extend_schema 

from .models import Student, Subject, ExamCategory, Exam, Score
from .serializers import *
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny] 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['roll_number', 'email', 'is_active']
    search_fields = ['name', 'roll_number', 'email', 'phone_number']
    ordering_fields = ['name', 'roll_number', 'created_at']
    ordering = ['name']

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code', 'credits']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'credits']
    ordering = ['code']

class ExamCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExamCategory.objects.all()
    serializer_class = ExamCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_mandatory']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'weightage']
    ordering = ['name']

class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'subject', 'status', 'date']
    search_fields = ['student__name', 'subject__name']
    ordering_fields = ['date', 'total_marks']
    ordering = ['-date']

    def get_queryset(self):
        return Exam.objects.all().select_related('student', 'subject')



class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['exam', 'category', 'graded_by']
    search_fields = ['remarks', 'graded_by', 'exam__student__name', 'category__name']
    ordering_fields = ['graded_at', 'marks']
    ordering = ['-graded_at']
