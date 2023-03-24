#!/bin/bash

SCRIPTDIR=$PWD

####### Create Base Images ############
cd ../builds/dbserver
docker build . --tag u2229437/db_base

cd ../webserver
docker build . --tag u2229437/web_base


####### Docker Slim ############
curl -sL https://raw.githubusercontent.com/slimtoolkit/slim/master/scripts/install-slim.sh | sudo -E bash -

slim build --target u2229437/web_base:latest --tag u2229437/web_slim:1 --include-path "/usr/share/nginx/html" --include-path "/etc/nginx/nginx.conf" --include-path "/etc/php.ini" --include-path "/etc/php-fpm.d/www.conf" --include-path "/etc/nginx/conf.d,/php-fpm.conf" --include-path "/docker-entrypoint.sh" --include-path "/var/log/nginx" --include-path "/var/log/apache" --include-path "/var/log/php-fpm" --include-path "/var/lib/nginx/tmp"
exit
slim build --target u2229437/db_base:latest --tag u2229437/db_slim:1 --http-probe=false --env "MYSQL_ROOT_PASSWORD="CorrectHorseBatteryStaple" --env "MYSQL_DATABASE="csvs23db" --include-path "/mysql/mysql.conf.d/mysqld.cnf" --include-path "/etc/mysql/conf.d/" --include-path "/bin/id"  --include-path "/run/mysqld/"
exit

#