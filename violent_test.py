import json
import subprocess
import requests
import time
import uuid

def unique_data():
    unique_id = uuid.uuid4()
    unique_id_hex = unique_id.hex
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

def test_case():
    tmp_fullname = unique_data()
    tmp_suggestion = unique_data()
    print("Name:", tmp_fullname, " Suggestion:", tmp_suggestion)
    result1=test_case_1(tmp_fullname, tmp_suggestion)
    result2=test_case_2(tmp_fullname, tmp_suggestion)
    print(result1)
    print(result2)
    return result1, result2


for i in range(50):
    result1, result2 = test_case()
    time.sleep(0.1)
    if result1 != 200 or result2 != 200:
        print("Test Failed!!!")

for i in range(1000):
    result1, result2 = test_case()
    if result1 != 200 or result2 != 200:
        print("Test Failed!!!")

