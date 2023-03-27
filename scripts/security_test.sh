# These commands should also be rewritten into security_test.py files for automated testing,
# but I don't have time to finish


####### Check SELinux ############

###### Check Syscalls ############


docker run --cpus=1 \
    --memory=256m --memory-swap=256m \
    --device-read-bps=/dev/sda:20mb --device-write-bps=/dev/sda:20mb \
    --security-opt seccomp:../builds/dbserver/u2229437-minimal-syscalls.json \
    --security-opt label:type:u2229437_docker_db_t \
    --cap-drop=ALL \
    -v db_mysql:/var/lib/mysql:rw \
    -d --net u2229437/csvs2023_n --ip 203.0.113.201 \
    --hostname db.cyber23.test -e MYSQL_ROOT_PASSWORD="CorrectHorseBatteryStaple" \
    -e MYSQL_DATABASE="csvs23db" --name u2229437_db u2229437/db_base

docker run --cpus=2 \
    --memory=128m --memory-swap=128m \
    --device-read-bps=/dev/sda:5mb --device-write-bps=/dev/sda:5mb \
    --security-opt seccomp:../builds/webserver/u2229437-minimal-syscalls.json \
    --security-opt label:type:u2229437_docker_web_t \
    --cap-drop=ALL \
    --cap-add CAP_NET_BIND_SERVICE \
    --cap-add CAP_CHOWN \
    --cap-add CAP_SETGID \
    --cap-add CAP_SETUID \
    -d --net u2229437/csvs2023_n --ip 203.0.113.200 \
    --hostname www.cyber23.test --add-host db.cyber23.test:203.0.113.201 \
    -p 80:80 --name u2229437_web u2229437/web_base 

docker exec u2229437_web chmod -R 777 /usr/share/nginx/html/
docker exec u2229437_db chmod -R 777 /etc/mysql

####### Check Capability ############
# 

docker run --cpus=1 \
    --memory=256m --memory-swap=256m \
    --device-read-bps=/dev/sda:20mb --device-write-bps=/dev/sda:20mb \
    --cap-drop=ALL \
    -v db_mysql:/var/lib/mysql:rw \
    -d --net u2229437/csvs2023_n --ip 203.0.113.201 \
    --hostname db.cyber23.test -e MYSQL_ROOT_PASSWORD="CorrectHorseBatteryStaple" \
    -e MYSQL_DATABASE="csvs23db" --name u2229437_db u2229437/db_base

docker run --cpus=2 \
    --memory=128m --memory-swap=128m \
    --device-read-bps=/dev/sda:5mb --device-write-bps=/dev/sda:5mb \
    --cap-drop=ALL \
    --cap-add CAP_NET_BIND_SERVICE \
    --cap-add CAP_CHOWN \
    --cap-add CAP_SETGID \
    --cap-add CAP_SETUID \
    -d --net u2229437/csvs2023_n --ip 203.0.113.200 \
    --hostname www.cyber23.test --add-host db.cyber23.test:203.0.113.201 \
    -p 80:80 --name u2229437_web u2229437/web_base

docker exec u2229437_web chown apache:apache /usr/share/nginx/html/index.php
docker exec u2229437_web chmod -R 777 /usr/share/nginx/html/
docker exec u2229437_db chmod -R 777 /etc/mysql