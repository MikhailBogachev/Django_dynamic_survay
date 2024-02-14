from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Survey(models.Model):
    """Модель опроса"""
    title = models.CharField(
        max_length=200
    )

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    """Модель вопроса"""
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE
    )
    text = models.TextField()

    def __str__(self) -> str:
        return self.text


class Choice(models.Model):
    """Модель варианта ответа"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices'
    )
    text = models.CharField(
        max_length=200
    )

    def __str__(self) -> str:
        return self.text


class NextQuestionLogic(models.Model):
    """Модель для формирования логики показа следующего вопроса"""
    prev_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='prev_question'
    )
    choice_to_the_prev_question = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    next_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='next_question'
    )
    default_next_question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='default_next_question'
    )


class SurveyResults(models.Model):
    """Модель результата опроса"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('user', 'survey', 'question')
