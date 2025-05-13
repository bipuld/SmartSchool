from django.db import models
from django.core.exceptions import ValidationError


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address=models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Indicates if student is currently enrolled")

    def __str__(self):
        return f"{self.name} ({self.roll_number})"

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['roll_number']),
        ]

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    credits = models.PositiveIntegerField(default=3, help_text="Credit hours for the subject")


    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        ordering = ['code']
        indexes = [
            models.Index(fields=['code']),
        ]

class ExamCategory(models.Model):
    name = models.CharField(max_length=100)
    weightage = models.FloatField(help_text="Weightage of this category (e.g., 20 for 20%)")
    description = models.TextField(blank=True, help_text="Details about the category (e.g., Quiz, Assignment)")
    is_mandatory = models.BooleanField(default=True, help_text="Is this category required for all exams?")

    def __str__(self):
        return f"{self.name} ({self.weightage}%)"

    def clean(self):
        if self.weightage < 0 or self.weightage > 100:
            raise ValidationError("Weightage must be between 0 and 100.")

    class Meta:
        ordering = ['name']

class Exam(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    total_marks = models.PositiveIntegerField(default=50,help_text="This is the full marks required for internal exam")
    date = models.DateField()
    status = models.CharField(max_length=20,choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],default='Scheduled')
    notes = models.TextField(blank=True, help_text="Additional exam notes")
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date}"

    class Meta:
        ordering = ['-date']
        indexes = [
            models.Index(fields=['student', 'subject']),
        ]

class Score(models.Model):
    exam = models.ForeignKey(Exam, related_name='scores', on_delete=models.CASCADE)
    category = models.ForeignKey(ExamCategory, on_delete=models.CASCADE)
    marks = models.FloatField()
    remarks = models.TextField(blank=True, help_text="Feedback or remarks for this score")
    graded_by = models.CharField(max_length=100, blank=True, help_text="Name of the grader")
    graded_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.exam} - {self.category} - {self.marks}"

    def save(self, *args, **kwargs):
        from django.utils import timezone
        max_marks = self.exam.total_marks * (self.category.weightage / 100)
        if self.marks > max_marks:
            raise ValidationError(f"Marks cannot exceed the maximum allowed ({max_marks}) for this category.")
        if self.marks < 0:
            raise ValidationError("Marks cannot be negative.")
        super().save(*args, **kwargs)



    def save(self,*args,**kwargs):
        self.clean()
        super().save(*args,**kwargs)

    class Meta:
        ordering = ['exam', 'category']
        unique_together = ('exam', 'category')
