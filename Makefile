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

reload:
	@make collectstatic
	touch reload

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
\t@echo "Installing requirements"
\t@pip install --exists-action=s -r requirements.txt