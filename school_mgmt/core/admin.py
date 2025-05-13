
# Register your models here.
from django.contrib import admin
from django.db.models import Sum
from django.urls import path
from django.http import HttpResponse
import csv
from .models import Student, Subject, ExamCategory, Exam, Score

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'roll_number', 'email', 'phone_number', 'is_active')
    list_filter = ('is_active', )
    search_fields = ('name', 'roll_number', 'email')
    list_editable = ('is_active',)
    date_hierarchy = 'created_at'
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ('name', 'roll_number', 'email')}),
        ('Contact Info', {'fields': ('phone_number', 'date_of_birth')}),
        ('Academic Info', {'fields': ['is_active']}), 
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('created_at', 'updated_at')  
    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "Selected students marked as active.")
    mark_active.short_description = "Mark selected students as active"

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "Selected students marked as inactive.")
    mark_inactive.short_description = "Mark selected students as inactive"

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credits')
    list_filter = ('name',)
    search_fields = ('name', 'code')
    ordering = ('name',)
    fieldsets = (
        (None, {'fields': ['name']}),
        ('Details', {'fields': ('code', 'credits')}),
    )

@admin.register(ExamCategory)
class ExamCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'weightage', 'is_mandatory', 'description')
    list_filter = ('is_mandatory',)
    search_fields = ('name', 'description')
    list_editable = ('weightage', 'is_mandatory')
    ordering = ('name',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'date', 'total_marks','status')
    list_filter = ('status', 'date', 'subject')
    search_fields = ('student__name', 'subject__name')
    date_hierarchy = 'date'
    list_editable = ('status',)
    ordering = ('-date',)
    raw_id_fields = ('student', 'subject')
    fieldsets = (
        (None, {'fields': ('student', 'subject', 'date')}),
        ('Details', {'fields': ('status', 'notes')}),
    )


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export-exams/', self.admin_site.admin_view(self.export_exams), name='exam_export'),
        ]
        return custom_urls + urls

    def export_exams(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exam_results.csv"'
        writer = csv.writer(response)
        writer.writerow(['Student', 'Subject', 'Date', 'Total Marks', 'Total Score', 'Weighted Score', 'Status'])
        for exam in Exam.objects.all():
            writer.writerow([
                exam.student.name if exam.student else '',
                exam.subject.name if exam.subject else '',
                exam.date,
                exam.total_marks,
                # exam.total_score() if hasattr(exam, 'total_score') else 0,
                # exam.weighted_score() if hasattr(exam, 'weighted_score') else 0,
                exam.status,
            ])
        return response
    export_exams.short_description = "Export exam results to CSV"


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ('exam', 'category', 'marks', 'graded_by', 'graded_at')
    list_filter = ('category', 'graded_at')
    search_fields = ('exam__student__name', 'exam__subject__name', 'graded_by')
    date_hierarchy = 'graded_at'
    ordering = ('-graded_at',)
    raw_id_fields = ('exam', 'category')
    readonly_fields = ('graded_at',)  

    fieldsets = (
        (None, {'fields': ('exam', 'category', 'marks')}), 
        ('Details', {'fields': ('remarks', 'graded_by')}),  
        ('Timestamps', {'fields': ('graded_at',)}),          
    )
