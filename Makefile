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
	@echo "Starting server ... "
	@make req
	@service nginx restart
	@uwsgi --ini uwsgi.ini

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
	@echo "Installing requirements"
	@sh install_nginx.sh
	@sh install_uwsgi.sh
	@apt -q -y install epel-release
	@apt -q -y install python36
	@apt -q -y install python36-setuptools
	@easy_install-3.6 pip
	@pip install --exists-action=s -r requirements.txt