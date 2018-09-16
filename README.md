# Python Developer - Homework #6

## Hasker

Веб-приложение на Django, система вопросов и ответов

Используется Python 3.6

### Deploy с помошью Docker-контейнера

1. Создаем Docker-контейнер на основе Dockerfile. Устанавливаются Ubuntu, git и make



    Запускем контейнер на localhost:8080:



    Вход в контейнер



2. Клонируем данный репозиторий в рабочую папку контейнера

   git clone https://github.com/aleksey-egorov/hasker

   Вход в hasker/ и запуск сборки приложения. Устанавливаются nginx, uWSGI, Python3.6, Postgres 10, Django 2.1, а также необходимые библиотеки.
   В процессе сборки надо будет указать географическую и временную зону, выбрав соответствующую цифру.

   cd hasker && make prod

3. Приложение должно быть доступно по адресу http://localhost:8080


