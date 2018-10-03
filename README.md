# Python Developer - Homework #6

## Hasker

Веб-приложение на Django, система вопросов и ответов

Используется Python 3.6


### Deploy с помошью Docker-контейнера

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

Приложение должно быть доступно по адресу http://localhost:8080 .

Для отправки почты из приложения вам необходимо будет остановить uWSGI, указать соответствующие реквизиты почты в hasker/custom.py,
после чего заново запустить сервер командой:

    uwsgi --ini /etc/uwsgi/apps-available/hasker.ini


