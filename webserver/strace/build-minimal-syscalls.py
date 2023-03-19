import json
import subprocess
import os
import requests
import time
import uuid

def create_minimal_json():
    # Read in the list of min-syscalls
    with open("list-of-min-syscalls", "r") as f:
        mini_syscalls = f.read().splitlines()
    # Read default sycalls
    with open("moby-default.json", "r") as f:
        default_syscalls = json.load(f)
    #creat mini json
    default_syscalls["syscalls"][0]["names"] = mini_syscalls
    with open("minimal-syscalls.json", "w") as f:
        json.dump(default_syscalls, f)

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

def get_minimal_syscalls():
    #call build-minimal-syscalls script
    #result=subprocess.call("sh $PWD/build-minimal-sycalls.sh",shell=True)
    # Read the list of syscalls from the file
    with open("./moby-syscalls", "r") as f:
        syscalls = f.readlines()
    
    tmp_path = "list-of-min-syscalls"
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
        subprocess.call("sh $PWD/minimal-sycalls-helper.sh",shell=True)

        # Run a Docker container with the updated Seccomp configuration
        cmd = "docker run --security-opt seccomp:tmp.json \
            -d --net u1234567/csvs2023_n --ip 203.0.113.200 --hostname www.cyber23.test \
            --add-host db.cyber23.test:203.0.113.201 -p 80:80 \
            --name u2229437_web_strace \
            u2229437/web_stripped "
        ret=os.system(cmd)
        time.sleep(3)

        tmp_fullname = unique_data()
        tmp_suggestion = unique_data()
        #test case 1
        result1=test_case_1(tmp_fullname, tmp_suggestion)
        #test case 2
        result2=test_case_2(tmp_fullname, tmp_suggestion)
        print(result1)
        print(result2)
        # If the container fails to start, log the current syscall to a file
        if ret != 0 or result1 != 200 or result2 != 200:
            with open("list-of-min-syscalls", "a") as f:
                f.write(f"{s}\n")
    #creat the minimal-syscalls-json
    create_minimal_json()
    return

def run_docker_with_minsyscalls():
    cmd="docker run --security-opt seccomp:minimal-syscalls.json \
        -d --net u1234567/csvs2023_n --ip 203.0.113.200 --hostname www.cyber23.test \
        --add-host db.cyber23.test:203.0.113.201 -p 80:80 \
        --name u2229437_web_strace \
        u2229437/web_stripped"
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode('utf-8')) 

#create_minimal_json()
run_docker_with_minsyscalls()
#get_minimal_syscalls()
