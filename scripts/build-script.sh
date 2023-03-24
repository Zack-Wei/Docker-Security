#!/bin/bash

SCRIPTDIR=$PWD

####### Set Envirment ############
# sudo yum -y install docker 
# sudo systemctl start docker.service

#Env SElinux
# sudo yum install selinux-policy-devel
# sudo vi /usr/lib/systemd/system/docker.service

#   # Modify one line from:
#   #     ExecStart=/usr/bin/dockerd
#   # To
#   #     ExecStart=/usr/bin/dockerd --selinux-enabled


####### Create Base Images ############
cd ../builds/dbserver
docker build --no-cache --tag u2229437/db_base  . 
sleep 2
cd ../webserver
docker build  --no-cache --tag u2229437/web_base .


# ####### Docker Slim ############
curl -sL https://raw.githubusercontent.com/slimtoolkit/slim/master/scripts/install-slim.sh | sudo -E bash -

slim build --target u2229437/web_base:latest --tag u2229437/web_slim:1 --include-path "/usr/share/nginx/html" --include-path "/etc/nginx/nginx.conf" --include-path "/etc/php.ini" --include-path "/etc/php-fpm.d/www.conf" --include-path "/etc/nginx/conf.d,/php-fpm.conf" --include-path "/docker-entrypoint.sh" --include-path "/var/log/nginx" --include-path "/var/log/apache" --include-path "/var/log/php-fpm" --include-path "/var/lib/nginx/tmp"
echo "Finished Web"
slim build --target u2229437/db_base:latest --tag u2229437/db_slim:1 --http-probe=false --env "MYSQL_ROOT_PASSWORD=\"CorrectHorseBatteryStaple\"" --env "MYSQL_DATABASE=\"csvs23db\"" --include-path "/mysql/mysql.conf.d/mysqld.cnf" --include-path "/etc/mysql/conf.d/" --include-path "/bin/id"  --include-path "/run/mysqld/"
echo "Finished DB"

#

