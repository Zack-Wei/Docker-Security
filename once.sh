####### Docker Network ############

# So that our containers can talk to each other, we need to create a docker network:

docker network create --subnet=203.0.113.0/24 u2229437/csvs2023_n


docker exec -i u2229437_db mysql -uroot -pCorrectHorseBatteryStaple < ../sqlconfig/csvs23db.sql



docker volume create db_mysql
