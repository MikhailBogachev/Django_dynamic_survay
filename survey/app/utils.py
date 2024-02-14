from .models import NextQuestionLogic, Question, Choice


def get_next_question(question: Question, choice: Choice) -> Question:
    """
    Получение следующего вопроса на основе логики в NextQuestionLogic.
    Если для выбранного варианта ответа предусматривается определенная
    логика, то возвращаем соответствующий вопрос.
    Иначе возвращаем дефолтный следующий вопрос.
    """
    logic = NextQuestionLogic.objects.filter(
        prev_question=question).first()
    if logic.choice_to_the_prev_question == choice:
        return logic.next_question
    else:
        return logic.default_next_question
