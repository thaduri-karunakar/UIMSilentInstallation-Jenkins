#!/usr/bin/env python
import os
import requests

# oc_uim_in_same_robot = os.getenv("oc_uim_in_same_robot").lower().strip()  # Value should be in yes or no
uim_domain_details = {}

def get_uim_domain_details():
    """ Start of UIM domain details api request """
    print("Collecting UIM domain details for ...")
    # if oc_uim_in_same_robot != "yes":
    # uim_domain_details = {}
    uim_home = "http://{}/uimapi/robots/v1".format(os.getenv("uim_ip"))     #http://10.173.32.160/uimapi/robots/v1
    print("The UI home url is : ", uim_home)
    # uim_home = "http://10.173.32.160/uimapi/robots/v1"
    # auth = ("administrator", "interOP@123")
    auth = (os.getenv("NIMBUS_USERNAME"), os.getenv("NIMBUS_PASSWORD"))
    print("NIMBUS_USERNAME : {} , NIMBUS_PASSWORD : {}".format(os.getenv("NIMBUS_USERNAME"), os.getenv("NIMBUS_PASSWORD")))
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
    # else:
    #
    #     print("Collecting UIM domain details for  UIM and OC in the same robot combination...")
    #     for key in ["ip", "domain", "hub", "robot", "address"]:
    #         uim_domain_details[key1] = value1
    #     if exit_code == 0:
    #         print("uimapi package deployed successfully on primary hub ... \n", stdout)
    #         print("Waiting for 3 minutes for wasp probe to come up ...")
    #         time.sleep(180)
    #     else:
    #         print("Failed to deploy uimapi package ... \n", stderr)
    #         sys.exit(1)



get_uim_domain_details()