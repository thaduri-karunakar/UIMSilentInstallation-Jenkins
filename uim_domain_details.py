import os
import requests
import robot_install
import oc_installer_properties


def get_uim_domain_details():
    """ Start of UIM domain details api request """
    uim_domain_details = {}
    uim_home = "http://{}/uimapi/robots/v1".format(os.getenv("uim_ip"))     #http://10.173.32.160/uimapi/robots/v1
    # uim_home = "http://10.173.32.160/uimapi/robots/v1"
    # auth = ("administrator", "interOP@123")
    auth = (os.getenv("NIMBUS_USERNAME"), os.getenv("NIMBUS_PASSWORD"))
    headers = {"Accept": "application/json", "Content-Type": "application/json;charset=UTF-8"}
    uim_request = requests.get(uim_home, auth=auth, headers=headers)
    res = (uim_request.json())
    # print(res)
    for key, value in res.items():
        for key1, value1 in value[0].items():
            if key1 in ["ip", "domain", "hub", "robot", "address"]:
                uim_domain_details[key1] = value1
    print("uim domain details are from uim_domain_details.py : ", uim_domain_details)

    """ End of UIM domain details api request """
    return uim_domain_details

get_uim_domain_details()