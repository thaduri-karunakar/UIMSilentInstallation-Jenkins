#!/usr/bin/env python
import os
import subprocess
import get_hostName_ip
import time

start = time.time()
uim_robot_ip = get_hostName_ip.get_ip()
uim_robot_hostname = get_hostName_ip.get_hostname()
uim_path = r"/{0}_domain/{0}_hub/{0}".format(uim_robot_hostname)
# uim_domain_details = uim_domain_details.get_uim_domain_details() #reading uim domain deatils  from uim_domain_details.py --> get_uim_domain_details
# print(uim_domain_details)
# uim_path = uim_domain_details["address"]
print("UIM Domain Path is : ", uim_path)
"""fresh_common_variables = ['MODE', 'HUB_ROBOT', 'NAS_PROBE', 'NIMBUS_USERNAME',
                          'SHORTCUT_STARTMENU', 'UMP_ROBOT_IP', 'MAINTENANCE_MODE_PROBE', 'SLA_ENGINE_PROBE',
                          'OC_AJP_PORT', 'OVERWRITE_DYNAMIC_VIEWS', 'WEBSERVICE_DASHBOARD_API', 'OC_HTTP_PORT',
                          'SHORTCUT_DESKTOP', 'DATA_ENGINE_PROBE', 'DISCOVERY_SERVER_PROBE', 'UMP_AJP_PORT',
                          'OC_ROBOT', 'USER_INSTALL_DIR', 'NIS_SERVER_PROBE', 'HUB_ROBOT_IP', 'UMP_ROBOT',
                          'WEBSERVICE_MOBILE', 'SERVICE_HOST_PROBE', 'UGS_PROBE', 'UMP_HTTP_PORT', 'NIMBUS_PASSWORD',
                          'RELATIONSHIP_SERVICES_PROBE', 'ACE_PROBE', 'MPSE_PROBE', 'OC_ROBOT_IP', 'ADE_PROBE']"""

installer_properties = {"MODE": os.getenv("MODE"), "NIMBUS_USERNAME": os.getenv("NIMBUS_USERNAME"), "NIMBUS_PASSWORD":
    os.getenv("NIMBUS_PASSWORD"), "HUB_ROBOT": uim_path, "HUB_ROBOT_IP": uim_robot_ip, "OC_ROBOT":
                        "{0}_domain/{0}_hub/{1}".format(uim_robot_hostname,os.getenv("OC_ROBOT_NAME")),
                        "UMP_ROBOT": "{0}_domain/{0}_hub/{1}".format(uim_robot_hostname, os.getenv("OC_ROBOT_NAME")),
                        "UMP_ROBOT_IP": os.getenv("OC_ROBOT_IP"), "OC_ROBOT_IP": os.getenv("OC_ROBOT_IP"),
                        "USER_INSTALL_DIR": os.getenv("USER_INSTALL_DIR"), "OC_HTTP_PORT": os.getenv("OC_HTTP_PORT"),
                        "UMP_HTTP_PORT": os.getenv("OC_HTTP_PORT"), "OC_AJP_PORT": os.getenv("OC_AJP_PORT"),
                        "UMP_AJP_PORT": os.getenv("OC_AJP_PORT"),
                        "SHORTCUT_STARTMENU": "true", "OVERWRITE_DYNAMIC_VIEWS": "true", "WEBSERVICE_DASHBOARD_API":
                        "true", "SHORTCUT_DESKTOP": "true", "WEBSERVICE_MOBILE": "true",
                        "NAS_PROBE": "{}/nas".format(uim_path),
                        "MAINTENANCE_MODE_PROBE": "{}/maintenance_mode".format(uim_path),
                        "SLA_ENGINE_PROBE": "{}/sla_engine".format(uim_path),
                        "DATA_ENGINE_PROBE": "{}/data_engine".format(uim_path),
                        "DISCOVERY_SERVER_PROBE": "{}/discovery_server".format(uim_path),
                        "NIS_SERVER_PROBE": "{}/nis_server".format(uim_path),
                        "SERVICE_HOST_PROBE": "{}/service_host".format(uim_path),
                        "UGS_PROBE": "{}/ugs".format(uim_path),
                        "RELATIONSHIP_SERVICES_PROBE": "{}/relationship_services".format(uim_path),
                        "ACE_PROBE": "{}/ace".format(uim_path), "MPSE_PROBE": "{}/mpse".format(uim_path),
                        "ADE_PROBE": "{}/automated_deployment_engine".format(uim_path)}


def get_oc_installer_properties():
    with open(r"\sw\Jenkins-slave\workspace\oc_installer.properties", "a") as pfile:
        for key, value in installer_properties.items():
            # print(key, value)
            # writing all variables into installer.properties file
            pfile.write('{}={}\n'.format(key, value))
    pfile.close()  # closing the file
    time.sleep(5)
    install_operator_console()
    print('Operator Console Installation has took', (time.time() - start) / 60, 'Minutes..')


def install_operator_console():
    oc_cmd = r"\sw\Jenkins-slave\workspace\oc-installer*.exe -i silent -f oc_installer.properties"
    cmd = subprocess.Popen(oc_cmd, shell=True, stderr=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    exit_code = cmd.wait()
    if exit_code == 0:
        print("operator console went Successfully : \n", stdout)
    else:
        print("operator console failed with below error : \n", stderr)


get_oc_installer_properties()
