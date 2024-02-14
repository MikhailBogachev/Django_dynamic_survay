from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from .models import Survey, Question, Choice, SurveyResults
from .utils import get_next_question


def show_surveys(request):
    """Страница со списком опросов"""
    surveys = Survey.objects.all()
    return render(request, 'surveys/surveys.html', {'surveys': surveys})

@login_required
def show_question(request, survey_id: int, question_id: int | None = None):
    """
    Страница с вопросом.
    При GET запросе выводим вопрос.
    При POST запросе сохраняем ответ, отрисовываем следующий вопрос.
    """
    survey = get_object_or_404(Survey, pk=survey_id)
    if question_id:
        question = Question.objects.filter(pk=question_id).first()
    else:
        question = Question.objects.filter(survey=survey).first()

    if request.method == 'POST':
        choice = None
        if 'choice' in request.POST:
            choice = get_object_or_404(Choice, pk=request.POST['choice'])
            result, _ = SurveyResults.objects.get_or_create(
                user=request.user, survey=survey, question=question
            )
            result.choice = choice
            result.save()

        next_question = get_next_question(question, choice)
        if next_question:
            return render(request, 'surveys/show_question.html',
                           {'survey': survey, 'question': next_question}
            )
        else:
            return show_results(request, survey_id)

    return render(request, 'surveys/show_question.html',
                   {'survey': survey, 'question': question}
    )


def show_results(request, survey_id: int):
    """
    Выводим статистику по опросу.
    """
    count_users = SurveyResults.objects.raw(
        '''
        SELECT 1 as id, COUNT(DISTINCT user_id) as count_users FROM app_surveyresults
        WHERE survey_id = %s
        ''',
        [survey_id]
    )[0].count_users

    questions = Survey.objects.raw(
        '''
        SELECT
            app_question.id,
            DENSE_RANK() OVER (ORDER BY COUNT(DISTINCT app_surveyresults.user_id) DESC) row_rank,
            app_question.text,
            COUNT(DISTINCT app_surveyresults.user_id) as count_users
        FROM app_question
        LEFT JOIN app_surveyresults
        ON app_question.id = app_surveyresults.question_id
        WHERE app_question.survey_id = %(survey_id)s
        GROUP BY app_question.id
        ''',
        {'survey_id': survey_id, 'count_users': count_users}
    )

    choices = Choice.objects.raw(
        '''
        SELECT
            app_question.id as question_id,
            app_choice.id,
            app_choice.text,
            COUNT(DISTINCT app_surveyresults.user_id) as count_users
        FROM app_choice
        LEFT JOIN app_question
        ON app_choice.question_id = app_question.id
        LEFT JOIN app_surveyresults
        ON app_choice.id = app_surveyresults.choice_id
        WHERE app_question.survey_id = %(survey_id)s
        GROUP BY app_question.id, app_choice.id
        ''',
        {'survey_id': survey_id}
    )

    return render(request, 'surveys/thanks.html',
                  {'cnt': count_users, 'questions': questions, 'choices': choices}
    )
