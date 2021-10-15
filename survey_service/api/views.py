from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .serializers import CompletedSurveySerilizer, SurveySerializer
from etc.models import Completed_survey, Survey
from .permissions import IsSafe
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from . import services


class SurveyViewSet(viewsets.ModelViewSet):
    '''Survey view set'''
    serializer_class = SurveySerializer
    permission_classes = [IsSafe]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        '''Admin can see all existing surveys.
        Users can see only valid surveys'''
        if self.request.user.is_superuser:
            return Survey.objects.all().order_by('end_date')
        return Survey.objects.filter(
            end_date__gt=timezone.now(),
            start_date__lt=timezone.now()
            )

    def retrieve(self, request, *args, **kwargs):
        '''Detail survey info'''
        survey_id = kwargs.get('pk')
        serializer = SurveySerializer(
            instance=get_object_or_404(Survey, pk=survey_id)
            )
        response = services.make_response_with_detailed_questions(
            serializer.data,
            survey_id
            )
        return Response(response)


class take_survey(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, **kwargs):
        '''Returns a template of JSON post
        request for answering the survey'''
        survey_id = kwargs.get('survey_id')
        questions_data = services.get_questions_data(survey_id)
        answer_tip = '<enter your answer instead of this row>'
        return Response(
            {
                'user': '',
                'answers': [
                    {
                        'question_id': question_id,
                        'answer': question_text + ' ' + answer_tip
                    } for question_id, question_text in questions_data
                    ]
            }
        )

    def post(self, request, **kwargs):
        '''Parses the POST request, then creates
        completed survey entity'''
        questions_status, user = services.parse_and_create_completed_survey(
            request,
            kwargs
            )
        return Response(
            {
                'answers': questions_status,
                'you can watch your comleted surveys here':
                    f'{request.get_host()}/api/v1/{user}/completed_surveys/'
            }
        )


class watch_completed_surveys(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, **kwargs):
        '''Shows completed surveys for specified user id'''
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
