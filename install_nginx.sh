echo "Installing nginx ... "

cat > /etc/yum.repos.d/nginx.repo << EOF
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/centos/$releasever/$basearch/
gpgcheck=0
enabled=1
EOF

yum update
yum install nginx
firewall-cmd --permanent --add-port=80/tcp
firewall-cmd --reload
systemctl enable nginx
systemctl start nginx