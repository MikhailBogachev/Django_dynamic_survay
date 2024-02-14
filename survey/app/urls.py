from django.urls import path
from .views import show_surveys, show_question


app_name = 'surveys'
urlpatterns = [
    path('surveys/', show_surveys, name='surveys'),
    path('survey/<int:survey_id>/show_question/<int:question_id>', show_question, name='show_question'),
    path('survey/<int:survey_id>/show_question/', show_question, name='show_first_question'),
]
