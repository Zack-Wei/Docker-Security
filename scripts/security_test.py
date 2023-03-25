import docker


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
pid_limits_web = 30
pid_limits_db = 30
read_limits_web = 0
write_limits_web = 0
read_limits_db = 20 * 1024 * 1024
write_limits_db = 20 * 1024 * 1024

## Get Cgroup limits from running container and give match result
# cpu
cpu_nano_web = container_web.attrs['HostConfig']['NanoCpus']
cpu_nano_db = container_db.attrs['HostConfig']['NanoCpus']

if cpu_nano_web == cpu_limits_web and cpu_nano_db == cpu_limits_db:
    print("CPU CHECK!")
else:
    print("CPU Limit Unmatch")

# memory
mem_web = container_web.attrs['HostConfig']['Memory']
memswap_web = container_web.attrs['HostConfig']['MemorySwap']
mem_db = container_db.attrs['HostConfig']['Memory']
memswap_db = container_db.attrs['HostConfig']['MemorySwap']

if mem_web == mem_limits_web and mem_db == mem_limits_db:
    print("Memory CHECK!")
else:
    print("Memory Limit Unmatch")

if memswap_web == memswap_limits_web and memswap_db == memswap_limits_db:
    print("SWAP CHECK!")
else:
    print("SWAP Limit Unmatch")

# pid
pid_web = container_web.attrs['HostConfig']['PidsLimit']
pid_db = container_db.attrs['HostConfig']['PidsLimit']

if pid_web == pid_limits_web and pid_db == pid_limits_db:
    print("PID CHECK!")
else:
    print("PID Limit Unmatch")

# device-read/write-bps
read_web = container_web.attrs['HostConfig']['BlkioDeviceReadBps'][0]['Rate']
write_web = container_web.attrs['HostConfig']['BlkioDeviceWriteBps'][0]['Rate']
read_db = container_db.attrs['HostConfig']['BlkioDeviceReadBps'][0]['Rate']
write_db = container_db.attrs['HostConfig']['BlkioDeviceWriteBps'][0]['Rate']

if read_web == read_limits_web and write_web == write_limits_web \
and read_db == read_limits_db and write_db == write_limits_db:
    print("IO CHECK!")
else:
    print("IO Limit Unmatch")


####### Check Network ############
# 


####### Check SELinux ############
# 


####### Check Syscalls ############
# 


####### Check Capability ############
# 


####### Check "security guy" code ############
# 


