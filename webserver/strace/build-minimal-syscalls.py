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

def test_case_3():
    #This case test 404
    url = "http://localhost/wrong_dic"
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        flag = str(e)[:3]
        if flag == "404":
            return 404
        else:
            return e

def test_case():
    tmp_fullname = unique_data()
    tmp_suggestion = unique_data()
    result1=test_case_1(tmp_fullname, tmp_suggestion)
    result2=test_case_2(tmp_fullname, tmp_suggestion)
    result3=test_case_3()
    print(result1)
    print(result2)
    print(result3)
    return result1, result2, result3

def run_docker_with_syscalls(sys_json):

    cmd=f"docker run --security-opt seccomp:{sys_json} \
        --security-opt label:type:docker_web_t --cap-drop=ALL \
        --cap-add CAP_CHOWN \
        --cap-add CAP_SETGID \
        --cap-add CAP_SETUID \
        --cap-add CAP_NET_BIND_SERVICE \
        --cap-add CAP_SYS_CHROOT \
        -d --net u2229437/csvs2023_n --ip 203.0.113.200 \
        --hostname www.cyber23.test --add-host db.cyber23.test:203.0.113.201 \
        -p 80:80 --name u2229437_web u2229437/web_base "

    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode


def get_minimal_syscalls():
    #call build-minimal-syscalls
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
        ret=run_docker_with_syscalls("tmp.json")
        time.sleep(2)
        print(ret)

        #test case
        result1, result2, result3 = test_case()

        # If the container fails to start, log the current syscall to a file
        if ret != 0 or result1 != 200 or result2 != 200 or result3 != 404:
            with open("list-of-min-syscalls", "a") as f:
                f.write(f"{s}\n")
    #creat the minimal-syscalls-json
    create_minimal_json()
    return

#create_minimal_json()
run_docker_with_syscalls("moby-default.json")
#test_case()
#get_minimal_syscalls()
