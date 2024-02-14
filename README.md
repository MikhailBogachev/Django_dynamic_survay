# Django_dynamic_survay
# Django сервис для прохождения опросов с динамическим отображением вопросов.

## Запуск сервиса
Необходимо использовать python 3.10 
1. Клонировать репозиторий:
```
git clone https://github.com/MikhailBogachev/Django_dynamic_survay.git
```

2. Gерейти в него в командной строке:
```
cd Django_dynamic_survay
```

3. Cоздать и активировать виртуальное окружение:
```
python -m venv env
```

```
source env/Scripts/activate
```
4. Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

5. Запустить сервер:
```
cd survey
```
```
python manage.py runserver
```
PS:  
Приложение будет доступно по адресу: http://127.0.0.1:8000/surveys/  
Для прохождения опроса необходимо зарегистрироваться.  
Я использовал SQLite по причине наличия в ее арсенале, необходимого для решения задания, функционала.  
Также я не стал исключать файл БД из загрузки на гит. Это позволит проверяющему быстрее проверить задания, т.к. исключаем необходимость выполнения миграций и наполнение БД данными.  
Для доступа к админке есть созданный супер_юзер (login: admin, password: admin).  

Логика динамического вывода вопросов описывается в модели NextQuestionLogic.  
- prev_question - вопрос на к-й дается ответ  
- choice_to_the_prev_question - вариант ответа на вопрос  
- next_question - вопрос, к-й следует вывести после текущего, при условии что выбран вариант ответа из choice_to_the_prev_question  
- default_next_question - вопрос. выводимый при несовпадении выбранного варианта ответа с choice_to_the_prev_question. Или если не указаны choice_to_the_prev_question и next_question.
