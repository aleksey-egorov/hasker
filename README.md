# Python Developer - Homework #6

## Hasker

Веб-приложение на Django, система вопросов и ответов

Используется Python 3.6


### Deploy с помощью Docker-контейнера

Создаем Docker-контейнер, для этого в папке с Dockerfile запускаем указанную команду. Устанавливаются Ubuntu, git и make

    docker build -t hasker .

Запускем контейнер на localhost:8080:

    docker run --rm -dit -p 8080:80 --name hasker hasker

Вход в контейнер

    docker exec -it hasker /bin/bash

Клонируем данный репозиторий в рабочую папку контейнера

    git clone https://github.com/aleksey-egorov/hasker

Вход в hasker/ и запуск сборки приложения. Устанавливаются nginx, uWSGI, Python3.6, Postgres 10, Django 2.1, а также необходимые библиотеки Python.
В процессе сборки надо будет указать географическую и временную зону, выбрав соответствующую цифру.

    cd hasker && make prod

После сборки приложение должно быть доступно по адресу http://localhost:8080


