#!/bin/bash
# find minimal syscalls by removing from default syscalls

while [ "$(docker ps -aqf "name=u2229437_db_strace")" ]
do
  docker kill $(docker ps -aqf "name=u2229437_db_strace")
  docker rm $(docker ps -aqf "name=u2229437_db_strace")
  sleep 0.5
done
