#!/bin/bash

SCRIPTDIR=$PWD
cd ../builds/

# DB
docker run  --cpus=1 --memory=256m --pids-limit=30 --device-read-bps=/dev/sda:10mb --device-write-bps=/dev/sda:10mb \
    --security-opt seccomp:dbserver/u2229437-minimal-syscalls.json \
    --security-opt label:type:u2229437_docker_db_t \
    --cap-drop=ALL \
    -v db_mysql:/var/lib/mysql:rw \
    -d --net u2229437/csvs2023_n --ip 203.0.113.201 \
    --hostname db.cyber23.test -e MYSQL_ROOT_PASSWORD="CorrectHorseBatteryStaple" \
    -e MYSQL_DATABASE="csvs23db" --name u2229437_db u2229437/db_slim:1

# WEB
docker run --cpus=1 --memory=128m --pids-limit=25 --device-read-bps=/dev/sda:10mb --device-write-bps=/dev/sda:10mb \
    --security-opt seccomp:webserver/u2229437-minimal-syscalls.json \
    --security-opt label:type:u2229437_docker_web_t \
    --cap-drop=ALL \
    --cap-add CAP_CHOWN \
    --cap-add CAP_NET_BIND_SERVICE \
    -d --net u2229437/csvs2023_n --ip 203.0.113.200 \
    --hostname www.cyber23.test --add-host db.cyber23.test:203.0.113.201 \
    -p 80:80 --name u2229437_web u2229437/web_slim:1

sleep 1


####### Service Test ############
# Give a test, insert 100 messages
cd $SCRIPTDIR
python3 service_test.py


####### Security Test ############
# Check Serurity Prolicy active or not 



    # --cap-add CAP_SETGID \
    # --cap-add CAP_SETUID \