from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from .serializers import CompletedSurveySerilizer, SurveySerializer
from etc.models import Completed_survey, Question, Survey, Answer
from .permissions import IsAdmin, IsSafe
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


class SurveyViewSet(viewsets.ModelViewSet):
    '''Survey view set'''
    serializer_class = SurveySerializer
    permission_classes = [IsSafe | IsAdmin]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Survey.objects.all().order_by('end_date')
        return Survey.objects.filter(end_date__gt=timezone.now(), start_date__lt=timezone.now())


class take_survey(APIView):
    def get(self, request, **kwargs):
        survey_id = kwargs.get('survey_id')
        survey = Survey.objects.get(pk=survey_id)
        question_ids = [question.id for question in survey.questions.all()]
        return Response(
            {
                'user': '<place for user id (optional)>',
                'answers': [
                    {
                        'question_id': question_id,
                        'answer':'<enter your answer here>'
                    }   for question_id in question_ids
                    ]
            }
        )


    def post(self, request, **kwargs):
        questions_status = {}
        user = request.data.get('user')
        survey = Survey.objects.get(pk=kwargs.get('survey_id'))
        answers = []
        if not user:
            user = 'annonymous'
        for ans in request.data['answers']:
            question_id = ans.get('question_id')
            answer = ans.get('answer')
            question = get_object_or_404(Question, id=question_id)
            if answer:
                answers.append(
                    Answer.objects.create(
                    question=question,
                    text=answer
                    )
                    )
                questions_status[question_id] = 'successfully saved'
        completed_survey = Completed_survey.objects.create(user=user, survey=survey)
        completed_survey.answers.set(answers)
        return Response(
            {
                'answers': questions_status,
                'watch your comleted surveys here': f'{request.get_host()}/api/v1/{user}/completed_surveys/'
            }
        )


class watch_completed_surveys(APIView):
    def get(self, request, **kwargs):
        user = kwargs.get('user_id')
        surveys = Completed_survey.objects.filter(user=user)
        if not surveys:
            return Response(
                {
                    'error': 'this id did not participate in any survey'
                }
            )
        serializer = CompletedSurveySerilizer(data=surveys, many=True)
        serializer.is_valid()
        return Response(serializer.data)