#!/bin/bash
# find minimal syscalls by removing from default syscalls

while [ "$(docker ps -aqf "name=u2229437_db")" ]
do
  echo "stop formar container with id:"
  docker kill $(docker ps -aqf "name=u2229437_db")
  docker rm $(docker ps -aqf "name=u2229437_db")
  sleep 0.5
  echo "rm unkilled volume:"
  docker volume rm $(docker volume ls -qf dangling=true)
done

echo "cleared formar container"