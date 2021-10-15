from django.contrib import admin
from .models import Completed_survey, Survey, Question


class QuestionInline(admin.TabularInline):
    model = Question


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    inlines = (QuestionInline, )

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs['exclude'] = ['start_date']
        return super(SurveyAdmin, self).get_form(request, obj, **kwargs)
