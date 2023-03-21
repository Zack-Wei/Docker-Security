# University of Warwick: Peter Norris: Feb 2023

# You will find two folders in this archive, one for a database container and one for a webserver container.
# This README file provides you with the commands to get the web application working in the most basic configuration.
# in all the following, replace u1234567 with your specific university ID.

# Updated by University of Warwick: Datong: Mar 2023 


####### Docker Network ############

# So that our containers can talk to each other, we need to create a docker network:

docker network create --subnet=203.0.113.0/24 u2229437/csvs2023_n

####### DATABASE (MySQL) ###########

# First build the database image from the supplied docker file. 
# Name your image u1234567/csvs2023-db_i  (but replace u1234567 with your own university id)
# (tag as 0.1, 0.2 as well as latest if you feel this to be essential).
# After building the MYSQL image from the dockerfile you can use the following run-time command to get started:

docker run -d --net u1234567/csvs2023_n --ip 203.0.113.201 --hostname db.cyber23.test -e MYSQL_ROOT_PASSWORD="CorrectHorseBatteryStaple" -e MYSQL_DATABASE="csvs23db" --name u1234567_csvs2023-db_c u1234567/csvs2023-db_i 

docker run -d --net u1234567/csvs2023_n --ip 203.0.113.201 --hostname db.cyber23.test -e MYSQL_ROOT_PASSWORD="CorrectHorseBatteryStaple" -e MYSQL_DATABASE="csvs23db" --name u1234567_csvs2023-db_test local/testdb:0.1

# After running this command, your mysql container will not be configured with a database.
# Therefore everytime you start your mysql container you need to run the following command in order to prepare the database:

docker exec -i u1234567_csvs2023-db_c mysql -uroot -pCorrectHorseBatteryStaple < sqlconfig/csvs23db.sql


# This will create a pre-configured database which can be used by the web application.

# NOTE 1: there should be no space between "-p" and your password (for example -ptest )
# NOTE 2: You will receive a MYSQL error if you attempt to run the 'docker exec' command too quickly after starting the container with 'docker run'. Wait for a few seconds so that database can get started.
# HINT: Importing your database everytime you start the container is not efficient... Think how you can make this data persist!
# NOTE 3: For information on the database image, see the following URL: https://hub.docker.com/_/mariadb

###### WEBSERVER (nginx)

# FIrst build the webserver image from the supplied dockerfile
# Name your image u1234567/csvs2023-web_i  (but replace u1234567 with your own university id)
# After building the NGINX dockerfile you can use the following run-time command to get started:

docker run -d --net u1234567/csvs2023_n --ip 203.0.113.200 --hostname www.cyber23.test --add-host db.cyber23.test:203.0.113.201 -p 80:80 --name u1234567_csvs2023-web_c u1234567/csvs2023-web_i

strip: 
docker run -d --net u1234567/csvs2023_n --ip 203.0.113.200 --hostname www.cyber23.test --add-host db.cyber23.test:203.0.113.201 -p 80:80 --name u2229437_web_stripped u2229437/web_stripped


strace:
docker build . --tag local/webstrace
/usr/bin/strace -ff -o /output/trace  -p $(pgrep -d',' -x strace)

docker run -d --net u1234567/csvs2023_n --ip 203.0.113.200 --hostname www.cyber23.test --add-host db.cyber23.test:203.0.113.201 -p 80:80 --name u1234567_csvs2023-webstrace --cap-add=SYS_PTRACE -v $PWD/output_h:/output_web:rw local/webstrace


/usr/bin/strace -ff -o /output/trace  -p $(pgrep -d',' -x strace)

# You should now be able to browse to http://localhost/ to view the web application!

# NOTE: If you have issues getting the basic setup working, ask for help!

# You can user script for quic start and test now!

