#!/bin/bash
# find minimal syscalls by removing from default syscalls

rm list-of-min-syscalls

while read s
do
  while [ "$(docker ps -aqf "name=u2229437_web_strace")" ]
  do
    docker kill $(docker ps -aqf "name=u2229437_web_strace")
    docker rm $(docker ps -aqf "name=u2229437_web_strace")
    sleep 0.5
  done

  echo "$s  being removed from moby-default.json"
  grep -v "\"${s}\"" ./moby-default.json > tmp.json
  
  docker run --security-opt seccomp:tmp.json \
  -d --net u1234567/csvs2023_n --ip 203.0.113.200 --hostname www.cyber23.test \
  --add-host db.cyber23.test:203.0.113.201 -p 80:80 \
  --name u2229437_web_strace \
  u2229437/web_stripped  || echo $s >> list-of-min-syscalls  

done < ./moby-syscalls

