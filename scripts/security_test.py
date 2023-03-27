import docker
import time
import subprocess
import json

# get local docker container env
client = docker.from_env()
container_web = client.containers.get('u2229437_web')
container_db = client.containers.get('u2229437_db')


####### Check Cgroup ############
# check point - setting cgroup
cpu_limits_web = 2000000000
cpu_limits_db = 1000000000
mem_limits_web = 128 * 1024 * 1024
mem_limits_db = 256 * 1024 * 1024
memswap_limits_web = 128 * 1024 * 1024
memswap_limits_db = 256 * 1024 * 1024
read_limits_web = 5 * 1024 * 1024
write_limits_web = 5 * 1024 * 1024
read_limits_db = 20 * 1024 * 1024
write_limits_db = 20 * 1024 * 1024
network_bridge_name = "u2229437/csvs2023_n"

## Get Cgroup limits from running container and give match result
# cpu
cpu_nano_web = container_web.attrs['HostConfig']['NanoCpus']
cpu_nano_db = container_db.attrs['HostConfig']['NanoCpus']

if cpu_nano_web == cpu_limits_web and cpu_nano_db == cpu_limits_db:
    print("CPU CHECK OK!")
else:
    print("CPU Limit Unmatch")

# memory
mem_web = container_web.attrs['HostConfig']['Memory']
memswap_web = container_web.attrs['HostConfig']['MemorySwap']
mem_db = container_db.attrs['HostConfig']['Memory']
memswap_db = container_db.attrs['HostConfig']['MemorySwap']

if mem_web == mem_limits_web and mem_db == mem_limits_db:
    print("Memory CHECK  OK!")
else:
    print("Memory Limit Unmatch")

if memswap_web == memswap_limits_web and memswap_db == memswap_limits_db:
    print("SWAP CHECK  OK!")
else:
    print("SWAP Limit Unmatch")

# device-read/write-bps
read_web = container_web.attrs['HostConfig']['BlkioDeviceReadBps'][0]['Rate']
write_web = container_web.attrs['HostConfig']['BlkioDeviceWriteBps'][0]['Rate']
read_db = container_db.attrs['HostConfig']['BlkioDeviceReadBps'][0]['Rate']
write_db = container_db.attrs['HostConfig']['BlkioDeviceWriteBps'][0]['Rate']

if read_web == read_limits_web and write_web == write_limits_web \
and read_db == read_limits_db and write_db == write_limits_db:
    print("IO CHECK OK!")
else:
    print("IO Limit Unmatch")

# network mode
network_web = container_web.attrs['HostConfig']['NetworkMode']
network_db = container_db.attrs['HostConfig']['NetworkMode']

if network_web == network_bridge_name and network_db == network_bridge_name:
    print("Network CHECK OK!")
else:
    print("Network Limit Unmatch")

####### Check "security guy" code ############
# 
chmod_result_web = container_web.exec_run('chmod -R 777 /usr/share/nginx/html/')
print(chmod_result_web.output.decode())

