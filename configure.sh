
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

cat > /home/work/hasker/hasker/components/secret.py << EOF
SECRET_KEY = '${SECRET}'
DB_PASSWORD = '${DB_PASSWORD}'
EOF

cd /home/work/hasker

source ~/.bashrc
/usr/bin/python3 manage.py makemigrations admin auth contenttypes sessions user question
/usr/bin/python3 manage.py migrate
