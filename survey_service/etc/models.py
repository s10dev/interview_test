from django.db import models


# Create your models here.
class Survey(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    description = models.TextField(max_length=300)

    def __str__(self):
        return self.title


class Question(models.Model):
    types_of_question = (
        ('ta', 'Text answer'),
        ('sca', 'Single choice answer'),
        ('mca', 'Multiple choice answer')
    )
    text = models.TextField(max_length=300)
    type = models.CharField(max_length=3, choices=types_of_question)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.TextField(max_length=300)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Completed_survey(models.Model):
    user = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT)
    answers = models.ManyToManyField(Answer, related_name='answers')

    def __str__(self):
        return self.survey.title
