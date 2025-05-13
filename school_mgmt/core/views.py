from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend # type: ignore
from rest_framework.permissions import AllowAny  
from drf_spectacular.utils import extend_schema 
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import Student, Subject, ExamCategory, Exam, Score
from .serializers import *



from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from .models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing student records.
    Supports filtering, searching, and ordering.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['roll_number', 'email', 'is_active']
    search_fields = ['name', 'roll_number', 'email', 'phone_number']
    ordering_fields = ['name', 'roll_number', 'created_at']
    ordering = ['name']

    @swagger_auto_schema(
        operation_description="Retrieve a list of students with optional filtering, searching, and ordering.",
        responses={
            200: StudentSerializer(many=True),
            400: "Bad Request",
            403: "Forbidden"
        },
        manual_parameters=[
            openapi.Parameter(
                'roll_number', openapi.IN_QUERY, description="Filter by roll number", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'email', openapi.IN_QUERY, description="Filter by email", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'is_active', openapi.IN_QUERY, description="Filter by active status", type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY, description="Search by name, roll_number, email, or phone_number", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering', openapi.IN_QUERY, description="Order by name, roll_number, or created_at (add - prefix to get the data in descending format)", type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class SubjectViewSet(viewsets.ModelViewSet):
    """
    This Class Handle the Overall Functionalities of Subject Details with fetures
    """
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['code', 'credits']
    search_fields = ['name', 'code']
    ordering_fields = ['name', 'code', 'credits']
    ordering = ['code']
    @swagger_auto_schema(
        operation_description=(
            "Retrieve a list of subjects with optional filtering, searching, and ordering.\n\n"
        ),
        responses={
            200: SubjectSerializer(many=True),
            400: "Bad Request",
            403: "Forbidden"
        },
        manual_parameters=[
            openapi.Parameter(
                'code', openapi.IN_QUERY, description="Filter by subject code", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'credits', openapi.IN_QUERY, description="Filter by credit hours", type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'search', openapi.IN_QUERY, description="Search by subject name or code", type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering', openapi.IN_QUERY,
                description="Order by `name`, `code`, or `credits`. Use '-' prefix for descending (e.g., `?ordering=-credits`)",
                type=openapi.TYPE_STRING
            ),
        ])
    def list(self,request,*args,**kwargs):
        return super().list(request,*args,**kwargs)



class ExamCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExamCategory.objects.all()
    serializer_class = ExamCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_mandatory']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'weightage']
    ordering = ['name']

    @swagger_auto_schema(
        operation_description="Retrieve a list of Exam Categories with optional filtering, searching, and ordering.",
        responses={
            200: ExamCategorySerializer(many=True),
            400: "Bad Request",
            403: "Forbidden"
        },
        manual_parameters=[
            openapi.Parameter(
                'is_mandatory',
                openapi.IN_QUERY,
                description="Filter by whether the category is mandatory (true/false)",
                type=openapi.TYPE_BOOLEAN
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by category name or description",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order by `name` or `weightage`. Use '-' for descending (e.g., `-weightage`)",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)





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
    
    @swagger_auto_schema(
        operation_description="Retrieve a list of Exams with optional filtering, searching, ordering, and pagination.",
        responses={
            200: ExamSerializer(many=True),
            400: "Bad Request",
            403: "Forbidden"
        },
        manual_parameters=[
            openapi.Parameter(
                'student',
                openapi.IN_QUERY,
                description="Filter by student ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'subject',
                openapi.IN_QUERY,
                description="Filter by subject ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="Filter by exam status (e.g., passed, failed)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'date',
                openapi.IN_QUERY,
                description="Filter by exact exam date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING,
                format=openapi.FORMAT_DATE
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by student name or subject name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order by `date` or `total_marks`. Use '-' for descending (e.g., `-date`, `-total_marks`)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Pagination page number",
                type=openapi.TYPE_INTEGER
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)



class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['exam', 'category', 'graded_by']
    search_fields = ['remarks', 'graded_by', 'exam__student__name', 'category__name']
    ordering_fields = ['graded_at', 'marks']
    ordering = ['-graded_at']

    @swagger_auto_schema(
        operation_description="Retrieve a list of Scores with optional filtering, searching, ordering, and pagination.",
        responses={
            200: ScoreSerializer(many=True),
            400: "Bad Request",
            403: "Forbidden"
        },
        manual_parameters=[
            openapi.Parameter(
                'exam',
                openapi.IN_QUERY,
                description="Filter by Exam ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter by Category ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'graded_by',
                openapi.IN_QUERY,
                description="Filter by the person who graded",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by remarks, graded_by, student name, or category name",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order by `graded_at`, `marks`. Use '-' for descending (e.g., `-marks`)",
                type=openapi.TYPE_STRING
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
