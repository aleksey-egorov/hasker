echo "*****"
echo "Installing nginx ... "

apt -q -y install nginx

cat > /etc/nginx/sites-available/hasker << EOF

upstream django {
     server unix:///tmp/hasker.sock;
}

server {
    listen      80;
    server_name     localhost;
    charset     utf-8;

    client_max_body_size 75M;

    location /media  {
        alias /home/work/hasker/media;
    }

    location /static {
        alias /home/work/hasker/static;

    }

    location / {
        uwsgi_pass  django;
        include     /etc/uwsgi/uwsgi_params;
    }
}
EOF

cd /etc/nginx/sites-enabled/
ln -fs /etc/nginx/sites-available/hasker hasker



echo "*****"
echo "Installing uWSGI ... "

apt-get -q -y install uwsgi

cat > /etc/uwsgi/apps-available/hasker.ini << EOF
[uwsgi]
uid = www-data
gid = www-data

chdir = /home/work/hasker
module = hasker.wsgi:application

master = true
processes = 1
socket = /tmp/hasker.sock
chmod-socket = 664
vacuum = true
plugins = python36
EOF

cd /etc/uwsgi/apps-enabled/
ln -fs /etc/uwsgi/apps-available/hasker.ini hasker

cat > /etc/uwsgi/uwsgi_params << EOF
uwsgi_param  QUERY_STRING       \$query_string;
uwsgi_param  REQUEST_METHOD     \$request_method;
uwsgi_param  CONTENT_TYPE       \$content_type;
uwsgi_param  CONTENT_LENGTH     \$content_length;

uwsgi_param  REQUEST_URI        \$request_uri;
uwsgi_param  PATH_INFO          \$document_uri;
uwsgi_param  DOCUMENT_ROOT      \$document_root;
uwsgi_param  SERVER_PROTOCOL    \$server_protocol;
uwsgi_param  REQUEST_SCHEME     \$scheme;
uwsgi_param  HTTPS              \$https if_not_empty;

uwsgi_param  REMOTE_ADDR        \$remote_addr;
uwsgi_param  REMOTE_PORT        \$remote_port;
uwsgi_param  SERVER_PORT        \$server_port;
uwsgi_param  SERVER_NAME        \$server_name;
EOF

chown -R www-data:www-data /home/work/hasker/



echo "*****"
echo "Installing Python3 ... "

apt-get -q -y install python3.6
apt-get -q -y install python3-pip
apt-get -q -y install uwsgi-plugin-python3
pip3 install --exists-action=s -r /home/work/hasker/requirements.txt



echo "*****"
echo "Installing PostgreSQL ... "

echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main" > /etc/apt/sources.list.d/pgdg.list
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
apt-get update
apt-get -q -y install postgresql-10
service postgresql start

# Postgres settings
DB_NAME=hasker
DB_USER=hasker
DB_PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 8 | head -n 1)

su postgres -c "psql -c \"DROP DATABASE IF EXISTS ${DB_NAME}\""
su postgres -c "psql -c \"DROP USER IF EXISTS ${DB_USER}\""
su postgres -c "psql -c \"CREATE USER ${DB_USER} PASSWORD '${DB_PASSWORD}'\""
su postgres -c "psql -c \"CREATE DATABASE ${DB_NAME} OWNER ${DB_USER}\""



echo "*****"
echo "Configuring Django ... "

SECRET=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)

cat > /home/work/hasker/hasker/secret.py << EOF
SECRET_KEY = '${SECRET}'
DB_PASSWORD = '${DB_PASSWORD}'
EOF

cd /home/work/hasker

/usr/bin/python3 manage.py makemigrations admin auth contenttypes sessions user question
/usr/bin/python3 manage.py migrate


