from etc.models import Survey, Answer, Completed_survey, Question
from django.shortcuts import get_object_or_404


def parse_and_create_completed_survey(request, kwargs):
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
    completed_survey = Completed_survey.objects.create(
        user=user,
        survey=survey
        )
    completed_survey.answers.set(answers)
    return questions_status, user


def get_questions_data(survey_id):
    survey = Survey.objects.get(pk=survey_id)
    questions_data = [
        (question.id, question.text) for question in survey.questions.all()
        ]
    return questions_data


def make_response_with_detailed_questions(serializer_data, survey_id):
    questions_data = get_questions_data(survey_id)
    response = serializer_data
    response['questions'] = [
        {
            'question_id': question_id,
            'question': question
        }
        for question_id, question in questions_data
    ]
    return response
