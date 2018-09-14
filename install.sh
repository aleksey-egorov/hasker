echo "*****"
echo "Installing nginx ... "

apt -q -y install nginx

cat > /etc/nginx/sites-available/hasker << EOF

upstream django {
     server unix:///etc/uwsgi/mysite.sock;
}

server {
    listen      80;
    server_name     hasker;
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
        include     /home/work/uwsgi_params;
    }
}

EOF

cd /etc/nginx/sites-enabled/
ln -fs /etc/nginx/sites-available/hasker hasker


echo "*****"
echo "Installing uWSGI ... "

apt-get -q -y install uwsgi


echo "*****"
echo "Installing Python3 ... "

apt-get -q -y install python3.6
apt-get -q -y install python3-pip


