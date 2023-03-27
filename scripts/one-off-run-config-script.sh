#!/bin/bash

SCRIPTDIR=$PWD
cd ../builds

####### Docker Network ############
# So that our containers can talk to each other, we need to create a docker network:
docker network create --subnet=203.0.113.0/24 u2229437/csvs2023_n


####### SE Linux ############
cd dbserver
# compile this textual file into an executable policy (.pp) file
sudo make -f /usr/share/selinux/devel/Makefile u2229437_docker_db.pp
sleep 1
# insert the policy file into the active kernel policies (ie so it can be used)
sudo semodule -i u2229437_docker_db.pp
cd ..

cd webserver
# compile this textual file into an executable policy (.pp) file
sudo make -f /usr/share/selinux/devel/Makefile u2229437_docker_web.pp
sleep 1
# insert the policy file into the active kernel policies (ie so it can be used)
sudo semodule -i u2229437_docker_web.pp
cd ..


####### Docker Volume ############
# Give a storage for database server
docker volume create db_mysql

####### Run the containers ############
# Run the containers
cd $SCRIPTDIR
./repeated-run-script.sh

# Prepare the database
# Because of the persistence volume, this cmd just need run once
sleep 20
cd ../builds/dbserver/
docker exec -i u2229437_db mysql -uroot -pCorrectHorseBatteryStaple < sqlconfig/csvs23db.sql
cd $SCRIPTDIR
sleep 1


####### Give a test ############
./testcase.sh



# ####### Run the slim containers ############
# cd $SCRIPTDIR
# ./rm_all_docker.sh
# sleep 1
# ./run-striped-container-script.sh