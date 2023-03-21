
#DB
docker run --security-opt label:type:docker_db_t --cap-drop=ALL \
    -d --net u2229437/csvs2023_n --ip 203.0.113.201 \
    --hostname db.cyber23.test -e MYSQL_ROOT_PASSWORD="CorrectHorseBatteryStaple" \
    -e MYSQL_DATABASE="csvs23db" --name u2229437_db u2229437/db_base 

sleep 12

docker exec -i u2229437_db mysql -uroot -pCorrectHorseBatteryStaple < dbserver/sqlconfig/csvs23db.sql

# WEB
docker run --security-opt label:type:docker_web_t --cap-drop=ALL \
    --cap-add CAP_CHOWN \
    --cap-add CAP_NET_BIND_SERVICE \
    --cap-add CAP_SETGID \
    --cap-add CAP_SETUID \
    -d --net u2229437/csvs2023_n --ip 203.0.113.200 \
    --hostname www.cyber23.test --add-host db.cyber23.test:203.0.113.201 \
    -p 80:80 --name u2229437_web u2229437/web_base
