echo "*****"
echo "Configuring Django ... "

SECRET=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 50 | head -n 1)

cat > /home/work/hasker/hasker/secret.py << EOF
SECRET_KEY = '${SECRET}'
DB_PASSWORD = '${DB_PASSWORD}'
EOF

cd /home/work/hasker

source ~/.bashrc
/usr/bin/python3 manage.py makemigrations admin auth contenttypes sessions user question
/usr/bin/python3 manage.py migrate
