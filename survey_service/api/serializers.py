from rest_framework import serializers
from etc.models import Completed_survey, Survey


class SurveySerializer(serializers.ModelSerializer):
    class Meta:
        model = Survey
        fields = '__all__'
        read_only_fields = ['start_date']


class CompletedSurveySerilizer(serializers.ModelSerializer):
    survey = serializers.CharField(source='survey.title', read_only=True)
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Completed_survey
        fields = '__all__'

    def get_answers(self, obj):
        response = []
        for el in obj.answers.all():
            response.append(
                {
                    'question': el.question.text,
                    'answer': el.text
                    }
                )
        return response
