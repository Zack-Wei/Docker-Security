#!/bin/bash
# find minimal syscalls by removing from default syscalls

while [ "$(docker ps -aqf "name=u2229437_web")" ]
do
  docker kill $(docker ps -aqf "name=u2229437_web")
  docker rm $(docker ps -aqf "name=u2229437_web")
  sleep 0.5
done
