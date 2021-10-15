# survey service API

Задача: спроектировать и разработать API для системы опросов пользователей.

Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

Использовать следующие технологии: Django 2.2.10, Django REST framework.

Результат выполнения задачи:
- исходный код приложения в github (только на github, публичный репозиторий)
- инструкция по разворачиванию приложения (в docker или локально)
- документация по API

## Getting Started

Для запуска сервиса необходимо выполнить команду "docker-compose up -d", затем загрузить фикстуры при помощи скрипта командой "./loadfixtures.sh"

Сервис будет доступен по адресу http://localhost/

## API documentation
Эндпоинты:
```
http://localhost/admin/ - панель администратора


http://localhost/api/v1/surveys/

[get] список доступных опросов


http://localhost/api/v1/surveys/<int:survey_id>/

[get] информация по определенному опросу, где survey_id это id опроса.


http://localhost/api/v1/surveys/<int:survey_id>/take_survey/

[get] json шаблон для прохождения опроса

[post] отправка ответов на опрос заполняя шаблон, полученного от get запроса


http://localhost/api/v1/<str:user_id>/comleted_surveys/

[get] просмотр пройденных пользователем user_id опросов и ответов на них
```
***

Функционал для администратора системы полностью реализован при помощи встроенной в Django панели администратора.  После установки фикстур, вы можете залогиниться по адресу http://localhost/admin как 123;123.

Пример использования функционала для пользователя системы:
1. Для получения списка активных опросов необходимо отправить get запрос на http://localhost/api/v1/surveys/  
2. Выбрав опрос из предоставленного ответа можно изучить его вопросы указав id опроса в адресе таким образом: http://localhost/api/v1/surveys/1/
3. Для прохождения выбранного опроса перейдите отправьте get запрос на http://localhost/api/v1/surveys/1/take_survey. В ответ придет готовый шаблон для ответов на выбранный опрос:
```json
{
    "user": "",
    "answers": [
        {
            "question_id": 1,
            "answer": "Как будете проводить выходные, если отключат интернет? <enter your answer instead of this row>"
        },
        {
            "question_id": 2,
            "answer": "А на острове без интернета чем займётесь? <enter your answer instead of this row>"
        },
    ]
}
```

Введя вместо поля "answer" свой ответ, необходимо отправить post запрос. В ответе будет содержаться информация об успешном (или нет) прохождении опроса.

4. Чтобы посмотреть пройденные пользователем опросы и ответы на них необходимо отправить get запрос на http://localhost/api/v1/123/completed_surveys, где "123" это индентификатор пользователя.

PS если не указать идентификатор во время прохождения отправки результатов опроса, то опрос автоматически запишется на пользователя annonymous. В таком случае, результаты можно также посмотреть при помощи метода, описанного ранее.

## Built With

* [nginx](https://nginx.org/ru/) - The web-server
* [PostgreSQL](https://www.postgresql.org/) - DB
* [Django](https://www.djangoproject.com/) - Python Framework

## Authors

* **S10dev** - *pet project* - [S10dev](https://github.com/s10dev)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
