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

class ScoreDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name')
    weightage = serializers.FloatField(source='category.weightage')
    max_marks = serializers.SerializerMethodField()


    class Meta:
        model = Score
        fields = ['category_name', 'weightage', 'marks', 'max_marks', 'graded_by', 'graded_at']

    def get_max_marks(self, obj):
        return obj.exam.total_marks * (obj.category.weightage / 100)
    
    def get_total_obtained_marks(self, obj):
        return sum(score.marks for score in obj.scores.all())
    

class ExamDetailSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    subject = SubjectSerializer()
    scores = ScoreDetailSerializer(many=True, read_only=True)
    total_obtained_marks = serializers.SerializerMethodField()
    class Meta:
        model = Exam
        fields = ['id', 'student', 'subject','notes', 'scores','status','date','total_obtained_marks','total_marks']

    def get_total_obtained_marks(self, obj):
        return sum(score.marks for score in obj.scores.all())