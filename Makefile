.PHONY: reload test syncdb migrate

MANAGE=`pwd`/manage.py
SETTINGS='core.settings.local'

update:
	@git stash
	@git pull
	@make req
	@make collectstatic
	@make migrate
	touch reload_project

prod:
	@make req
	@echo "Starting server ... "
	@service nginx start
	@uwsgi --ini /etc/uwsgi/apps-available/hasker.ini

test:
	DJANGO_SETTINGS_MODULE=$(SETTINGS) ./manage.py test

run:
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) runserver 0.0.0.0:8880

_makemigrations:
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) makemigrations

migrate:
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) migrate

collectstatic:
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) collectstatic --noinput

req:
	@echo "Installing requirements ..."
	@sh build.sh
	@sh configure.sh

