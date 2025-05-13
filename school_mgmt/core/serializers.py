from rest_framework import serializers
from .models import Student, Subject, ExamCategory, Exam, Score

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ExamCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamCategory
        fields = '__all__'

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ScoreSerializer(serializers.ModelSerializer):
    exam_info = serializers.StringRelatedField(source='exam', read_only=True)
    category_info = serializers.StringRelatedField(source='category', read_only=True)

    class Meta:
        model = Score
        fields = '__all__'
        read_only_fields = ['graded_at']
