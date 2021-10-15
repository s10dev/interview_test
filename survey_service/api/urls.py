from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import \
    (obtain_jwt_token, refresh_jwt_token, verify_jwt_token)


router = DefaultRouter()
router.register('surveys', views.SurveyViewSet, 'Survey')

urlpatterns = [
    path('', include(router.urls)),
    path('surveys/<int:survey_id>/take_survey/', views.take_survey.as_view()),
    path('<str:user_id>/completed_surveys/', views.watch_completed_surveys.as_view()),
    path('api-token-auth/', obtain_jwt_token),
    path('api-token-refresh/', refresh_jwt_token),
    path('api-token-verify/', verify_jwt_token),
]
