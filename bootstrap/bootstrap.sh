#!/bin/bash

# install and start nginx
sudo amazon-linux-extras install -y nginx1
sudo aws s3 cp s3://pierogis.live/bootstrap/pierogis-live.conf /etc/nginx/conf.d/pierogis-live.conf

# install the gunicorn app as a system service
sudo aws s3 cp s3://pierogis.live/bootstrap/pierogis-live.service /etc/systemd/system/pierogis-live.service
sudo chmod 755 /etc/systemd/system/pierogis-live.service
sudo systemctl daemon-reload

# install python
sudo yum install -y python3 python3-devel gcc postgresql-devel

# add the pierogis-live user
sudo useradd pierogis-live
sudo passwd -f -u pierogis-live

# copy server install script
echo export VERSION=$(aws ssm get-parameter --name 'version' --query 'Parameter.Value') >> /etc/profile
sudo aws s3 cp s3://pierogis.live/dist/pierogis-live-$VERSION.tar.gz /home/pierogis-live/pierogis-live.tar.gz

# install the python packages as pierogis-live user
sudo python3 -m venv /home/pierogis-live/venv
sudo /home/pierogis-live/venv/bin/pip install gunicorn
sudo /home/pierogis-live/venv/bin/pip install /home/pierogis-live/pierogis-live.tar.gz

# configure gunicorn
sudo aws s3 cp s3://pierogis.live/bootstrap/gunicorn.conf.py /home/pierogis-live/conf/gunicorn.conf.py
sudo chown pierogis-live:pierogis-live /var/log/gunicorn.error.log
sudo chown pierogis-live:pierogis-live /var/log/gunicorn.access.log

# make pierogis-live the owner of the application folder
sudo chown pierogis-live:pierogis-live /home/pierogis-live

# allow nginx to access pierogis-live user home folder
sudo chmod 710 /home/pierogis-live/
sudo usermod -a -G pierogis-live nginx

echo export CONTENT_HOME=$(aws ssm get-parameter --name 'content-home' --query 'Parameter.Value') >> /etc/profile
echo export BOOTSTRAP_HOME=$(aws ssm get-parameter --name 'bootstrap-home' --query 'Parameter.Value') >> /etc/profile
echo export DIST_HOME=$(aws ssm get-parameter --name 'dist-home' --query 'Parameter.Value') >> /etc/profile
echo export DATABASE_URL=$(aws ssm get-parameter --name 'database-url' --query 'Parameter.Value') >> /etc/profile

source /etc/profile

# start the server and nginx
sudo systemctl start pierogis-live
sudo systemctl enable pierogis-live
sudo systemctl start nginx
sudo systemctl enable nginx