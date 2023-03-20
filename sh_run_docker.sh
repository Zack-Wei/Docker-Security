
#DB
docker run --security-opt label:type:docker_db_t --cap-drop=ALL \
    -d --net u1234567/csvs2023_n --ip 203.0.113.201 \
    --hostname db.cyber23.test -e MYSQL_ROOT_PASSWORD="CorrectHorseBatteryStaple" \
    -e MYSQL_DATABASE="csvs23db" --name u1234567_csvs2023-db_c u1234567/csvs2023-db_i 

sleep 10

docker exec -i u1234567_csvs2023-db_c mysql -uroot -pCorrectHorseBatteryStaple < dbserver/sqlconfig/csvs23db.sql

# WEB
docker run --security-opt label:type:docker_web_t \
    --rm -d --net u1234567/csvs2023_n --ip 203.0.113.200 \
    --hostname www.cyber23.test --add-host db.cyber23.test:203.0.113.201 \
    -p 80:80 --name u1234567_csvs2023-web_c u1234567/csvs2023-web_i

#