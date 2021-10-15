from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('surveys', views.SurveyViewSet, 'Survey')

urlpatterns = [
    path('', include(router.urls)),
    path('surveys/<int:survey_id>/take_survey/', views.take_survey.as_view()),
    path('<str:user_id>/completed_surveys/', views.watch_completed_surveys.as_view()),
]
