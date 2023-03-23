
#DB
docker run  --cpus=1 --memory=256m --pids-limit=30 --device-read-bps=/dev/sda:10mb --device-write-bps=/dev/sda:10mb \
    --security-opt seccomp:dbserver/strace/minimal-syscalls.json \
    --security-opt label:type:docker_db_t \
    --cap-drop=ALL \
    -v db_mysql:/var/lib/mysql:rw \
    -d --net u2229437/csvs2023_n --ip 203.0.113.201 \
    --hostname db.cyber23.test -e MYSQL_ROOT_PASSWORD="CorrectHorseBatteryStaple" \
    -e MYSQL_DATABASE="csvs23db" --name u2229437_db u2229437/db_slim:1

# sleep 15
# docker exec -i u2229437_db mysql -uroot -pCorrectHorseBatteryStaple < dbserver/sqlconfig/csvs23db.sql

# #WEB
# docker run  --cpus=1 --memory=128m --pids-limit=25 --device-read-bps=/dev/sda:10mb --device-write-bps=/dev/sda:10mb \
#     --security-opt seccomp:webserver/strace/minimal-syscalls.json \
#     --security-opt label:type:docker_web_t \
#     --cap-drop=ALL \
#     --cap-add CAP_CHOWN \
#     --cap-add CAP_NET_BIND_SERVICE \
#     --cap-add CAP_SETGID \
#     --cap-add CAP_SETUID \
#     -d --net u2229437/csvs2023_n --ip 203.0.113.200 \
#     --hostname www.cyber23.test --add-host db.cyber23.test:203.0.113.201 \
#     -p 80:80 --name u2229437_web u2229437/web_slim:1


#build --target u2229437/web_base:latest --tag u2229437/web_slim:1 --include-path "/usr/share/nginx/html" --include-path "/etc/nginx/nginx.conf" --include-path "/etc/php.ini" --include-path "/etc/php-fpm.d/www.conf" --include-path "/etc/nginx/conf.d,/php-fpm.conf" --include-path "/docker-entrypoint.sh" --include-path "/var/log/nginx" --include-path "/var/log/apache" --include-path "/var/log/php-fpm" --include-path "/var/lib/nginx/tmp"

#build --target u2229437/db_base:latest --tag u2229437/db_slim:1 --http-probe=false --env "MYSQL_ROOT_PASSWORD="CorrectHorseBatteryStaple" --env "MYSQL_DATABASE="csvs23db"  --include-path "/mysql/mysql.conf.d/mysqld.cnf" --include-path "/etc/mysql/conf.d/" --include-path "/bin/id"  --include-path "/run/mysqld/"