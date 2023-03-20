import json
import subprocess
import requests
import time
import os
import uuid
import random
import docker
import subprocess

Probability = 0.5

def create_minimal_json(listname):
    # Read in the list of min-syscalls
    with open(listname, "r") as f:
        mini_syscalls = f.read().splitlines()
    # Read default sycalls
    with open("moby-default.json", "r") as f:
        default_syscalls = json.load(f)
    #creat mini json
    default_syscalls["syscalls"][0]["names"] = mini_syscalls

    with open(f"{listname}.json", "w") as f:
        json.dump(default_syscalls, f)

def kill_and_rm():
    subprocess.call("sh $PWD/minimal-sycalls-helper.sh",shell=True)
    pass

def insert_sql_config():
    time.sleep(8)
    cmd = "docker exec -i u2229437_db_strace mysql -uroot -pCorrectHorseBatteryStaple < ../sqlconfig/csvs23db.sql"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    timeout = 1
    start_time = time.time()
    while proc.poll() is None:
        time.sleep(0.1)
        if time.time() - start_time > timeout:
            proc.terminate()
            print("External program timed out, starting program A...")
            
            return

def run_docker_with_syscalls(syscalls_json):
    cmd = f"docker run --security-opt seccomp:{syscalls_json} \
        -d --net u1234567/csvs2023_n --ip 203.0.113.201 --hostname db.cyber23.test \
        -e MYSQL_ROOT_PASSWORD=\"CorrectHorseBatteryStaple\" -e MYSQL_DATABASE=\"csvs23db\" \
        --name u2229437_db_strace u2229437/db_strip_base "

    ret = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("ret1:", ret.returncode)

    if ret.returncode == 0:
        insert_sql_config()
    else:
        print("docker start failed")
    return ret.returncode

def unique_data():
    unique_id = uuid.uuid4()
    unique_id_hex = unique_id.hex
    print(unique_id_hex)
    return unique_id_hex

def test_case_1(fullname, suggestion):
    #This case test POST
    data={'fullname':fullname,'suggestion':suggestion}
    url = "http://localhost/action.php"
    try:
        response = requests.post(url, data=data, timeout=3)
        response.raise_for_status()
        return response.status_code
    except requests.exceptions.RequestException as e:
        return e

def test_case_2(fullname, suggestion):
    #This case test GET
    url = "http://localhost/index.php"
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        # Search the data write before
        if fullname in response.text and suggestion in response.text:
            return response.status_code
        return "fail db insert "
    except requests.exceptions.RequestException as e:
        return e

def half_the_syscalls(original_list):
    with open(original_list, "r") as f:
        syscalls = f.readlines()
    #delete exist moby-syscalls-dich file
    tmp_path = "tmp-dich"
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
    # delete half syscalls randomly
    random.shuffle(syscalls)
    syscalls = syscalls[:int(len(syscalls)*Probability)]

    #write in the list file
    for s in syscalls:
        s = s.strip()
        with open("tmp-dich", "a") as f:
            f.write(f"{s}\n")
    #creat dich json
    create_minimal_json("tmp-dich")

def dichotomy_to_get_mini_syscalls():
    # give 10 times test
    half_the_syscalls("moby-dich-syscalls")
    for i in range(10):
        #kill and rm exit docker before new run
        kill_and_rm()

        # Run a Docker container with the half Seccomp configuration
        ret=run_docker_with_syscalls("tmp-dich.json")

        #test case 
        tmp_fullname = unique_data()
        tmp_suggestion = unique_data()
        result1=test_case_1(tmp_fullname, tmp_suggestion)
        result2=test_case_2(tmp_fullname, tmp_suggestion)
        print(result1)
        print(result2)
        # If the container fails to start, log the current syscall to a file
        if ret == 0 and result1 == 200 and result2 == 200:
            half_the_syscalls("tmp-dich")
            print("Succeed after", i+1, "times trying")
            return
        else:
            half_the_syscalls("moby-dich-syscalls")

def get_minimal_syscalls():

    with open("./moby-syscalls", "r") as f:
        syscalls = f.readlines()
    tmp_path = "minimal-syscalls"
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    for s in syscalls:
        s = s.strip()
        print(s)
        # # Remove the current syscall from the JSON file
        with open("moby-default.json", "r") as f:
            tmp_syscalls = json.load(f)
        tmp_syscalls["syscalls"][0]["names"].remove(s)
        with open("tmp.json", "w") as f:
            f.write(json.dumps(tmp_syscalls))  
        #kill and rm exit docker before new run
        kill_and_rm()

        ret=run_docker_with_syscalls("tmp.json")

        tmp_fullname = unique_data()
        tmp_suggestion = unique_data()
        #test case
        result1=test_case_1(tmp_fullname, tmp_suggestion)
        result2=test_case_2(tmp_fullname, tmp_suggestion)
        print(result1)
        print(result2)
        # If the container fails to start, log the current syscall to a file
        if ret != 0 or result1 != 200 or result2 != 200:
            with open("minimal-syscalls", "a") as f:
                f.write(f"{s}\n")
    #creat the minimal-syscalls-json
    create_minimal_json("minimal-syscalls")
    return


#create_minimal_json()
#run_docker_with_syscalls("tmp-dich.json")
#dichotomy_to_get_mini_syscalls()
get_minimal_syscalls()

