import requests
import time
import os


base_url = r"https://cloudportal.broadcom.net/api/vms"
header = {"X-Auth-Token": "38377c9bc6612337cc48d55928548488"}
host_ids = {}


def test_get_vms():
    payload = \
        {
            'expand': 'resources',
            'attributes': 'name'
        }
    response = requests.get("{}?".format(base_url), params=payload, headers=header)
    #response = requests.get("{}?".format(base_url), params=payload, auth = uim_credentials)
    print("\nResponse URL is :", response.url)
    print("\nResponse Code is : ", response.status_code)
    assert response.status_code == 200
    res_dict = response.json() # response dictionary with all vm details
    #print(res_dict)
    for key, value in res_dict.items():
        if key == 'resources':
            for key1 in value:
                #print(key1)
                for key2, value2 in key1.items():
                    if key2.startswith("href"):
                        continue
                    # print(key2, '-->', value2)
                    if key2.startswith("name"):
                        host = value2
                        # print(value2)
                    if key2.startswith("id"):
                        id = value2
                        # print(value2)
                    host_ids[host] = value2
    time.sleep(5)
    print(host_ids)


def take_vm_snapshot():
    data = \
        {

            "action": "take snapshot",
            "snap_name": "CleanImage"
        }
    headers = {"X-Auth-Token": "38377c9bc6612337cc48d55928548488", 'Accept': '*/*', 'Content-Type': 'text/plain',
               'Content-Type': 'application/json'}
    host = os.getenv("host_name").strip()
    vm_id = host_ids[host]
    print("Snapshot vm id is : ", vm_id, "for host : ", host)

    response = requests.post("{}/{}".format(base_url, vm_id), json=data, headers=headers)
    print("\nResponse URL is :", response.url)
    print("\nResponse Code is : ", response.status_code)
    assert response.status_code == 200
    res = response.json()
    print(res)
    print("\n{} VM snapshot will be ready in few minutes...".format(host))


def revert_vm_snapshot():

    data = \
        {
            "action": "revert snapshot",
            "snapshot_uuid": "CleanImage"
        }
    headers = {"X-Auth-Token": "38377c9bc6612337cc48d55928548488", 'Accept': '*/*', 'Content-Type': 'text/plain',
               'Content-Type': 'application/json'}
    host = os.getenv("host_name").strip()
    print(host)
    vm_id = host_ids[host]
    print("Snapshot vm id is : ", vm_id, "for host : ", host)

    response = requests.post("{}/{}".format(base_url, vm_id), json=data, headers=headers)
    print("\nResponse URL is :", response.url)
    print("\nResponse Code is : ", response.status_code)
    assert response.status_code == 200
    res = response.json()
    print(res)
    print("\n{} VM snapshot will be revert  in few minutes and vm will get restarted...".format(host))

def vm_power_state():

    data = \
        {
            "action": os.getenv("state")   #state should be start or stop
        }
    headers = {"X-Auth-Token": "b1c974255458934ac4143b3446e6cf95", 'Accept': '*/*', 'Content-Type': 'text/plain',
               'Content-Type': 'application/json'}
    host = os.getenv("host_name").strip().lower()
    print(host)
    if host == "all_vms":
        for host in host_ids.keys():
            vm_id = host_ids[host]
            print("vm id is : ", vm_id, "for host : ", host, "to power ", os.getenv("state"))

            response = requests.post("{}/{}".format(base_url, vm_id), json=data, headers=headers)
            print("\nResponse URL is :", response.url)
            print("\nResponse Code is : ", response.status_code)
            assert response.status_code == 200
            res = response.json()
            print(res)
            print("\n{} VM will power {} in couple of minutes...".format(host, os.getenv("state")))
            time.sleep(2)
    else:
        vm_id = host_ids[host]
        print("vm id is : ", vm_id, "for host : ", host, "to power ", os.getenv("state"))
        response = requests.post("{}/{}".format(base_url, vm_id), json=data, headers=headers)
        print("\nResponse URL is :", response.url)
        print("\nResponse Code is : ", response.status_code)
        assert response.status_code == 200
        res = response.json()
        print(res)
        print("\n{} VM will power {} in couple of minutes...".format(host, os.getenv("state")))


test_get_vms()
user_input = os.getenv("method_to_call").strip()
if user_input == "take_vm_snapshot":
    take_vm_snapshot()
elif user_input == "revert_vm_snapshot":
    revert_vm_snapshot()
elif user_input == "power_state":
    vm_power_state()
else:
    print("Please provide valid user_input [take_vm_snapshot / revert_vm_snapshot")
    exit(1)
