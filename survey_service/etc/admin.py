from django.contrib import admin
from .models import Completed_survey, Survey, Question

class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    inlines = (QuestionInline, )

@admin.register(Completed_survey)
class CompletedSurveyAdmin(admin.ModelAdmin):
    pass