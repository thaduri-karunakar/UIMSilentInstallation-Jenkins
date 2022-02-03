#!/usr/bin/env python
import os
import subprocess
import get_hostName_ip
import time


start = time.time()

uim_host_ip = get_hostName_ip.get_ip()
uim_hostname = get_hostName_ip.get_hostname()
uim_path = r"/{}_domain/{}_hub/{}".format(uim_hostname, uim_hostname, uim_hostname)
fresh_common_variables = ['MODE', 'HUB_ROBOT', 'NAS_PROBE', 'NIMBUS_USERNAME',
                          'SHORTCUT_STARTMENU', 'UMP_ROBOT_IP', 'MAINTENANCE_MODE_PROBE', 'SLA_ENGINE_PROBE',
                          'OC_AJP_PORT', 'OVERWRITE_DYNAMIC_VIEWS', 'WEBSERVICE_DASHBOARD_API', 'OC_HTTP_PORT',
                          'SHORTCUT_DESKTOP', 'DATA_ENGINE_PROBE', 'DISCOVERY_SERVER_PROBE', 'UMP_AJP_PORT',
                          'OC_ROBOT', 'USER_INSTALL_DIR', 'NIS_SERVER_PROBE', 'HUB_ROBOT_IP', 'UMP_ROBOT',
                          'WEBSERVICE_MOBILE', 'SERVICE_HOST_PROBE', 'UGS_PROBE', 'UMP_HTTP_PORT', 'NIMBUS_PASSWORD',
                          'RELATIONSHIP_SERVICES_PROBE', 'ACE_PROBE', 'MPSE_PROBE', 'OC_ROBOT_IP', 'ADE_PROBE']

installer_properties = {"MODE": os.getenv("MODE"), "NIMBUS_USERNAME": os.getenv("NIMBUS_USERNAME"), "NIMBUS_PASSWORD":
                        os.getenv("NIMBUS_PASSWORD"), "HUB_ROBOT": uim_path, "HUB_ROBOT_IP": uim_host_ip, "OC_ROBOT":
                        "{}_domain/{}_hub/{}".format(uim_hostname, uim_hostname, os.getenv("OC_ROBOT")), "UMP_ROBOT":
                         "{}_domain/{}_hub/{}".format(uim_hostname, uim_hostname, os.getenv("OC_ROBOT")),
                        "UMP_ROBOT_IP": os.getenv("OC_ROBOT_IP"), "OC_ROBOT_IP": os.getenv("OC_ROBOT_IP"),
                        "USER_INSTALL_DIR": os.getenv("USER_INSTALL_DIR"), "OC_HTTP_PORT": os.getenv("OC_HTTP_PORT"),
                        "UMP_HTTP_PORT": os.getenv("OC_HTTP_PORT"), "OC_AJP_PORT": os.getenv("OC_AJP_PORT"), "UMP_AJP_PORT": os.getenv("OC_AJP_PORT"),
                        "SHORTCUT_STARTMENU": "true", "OVERWRITE_DYNAMIC_VIEWS": "true", "WEBSERVICE_DASHBOARD_API":
                        "true", "SHORTCUT_DESKTOP": "true", "WEBSERVICE_MOBILE": "true", "NAS_PROBE": "{}/nas".format(uim_path),
                        "MAINTENANCE_MODE_PROBE": "{}/maintenance_mode".format(uim_path), "SLA_ENGINE_PROBE": "{}/sla_engine".format(uim_path), "DATA_ENGINE_PROBE": "{}/data_engine".format(uim_path), "DISCOVERY_SERVER_PROBE": "{}/discovery_server".format(uim_path),
                        "NIS_SERVER_PROBE": "{}/nis_server".format(uim_path), "SERVICE_HOST_PROBE": "{}/service_host".format(uim_path), "UGS_PROBE": "{}/ugs".format(uim_path), "RELATIONSHIP_SERVICES_PROBE": "{}/relationship_services".format(uim_path),
                        "ACE_PROBE": "{}/ace".format(uim_path), "MPSE_PROBE": "{}/mpse".format(uim_path), "ADE_PROBE": "{}/automated_deployment_engine".format(uim_path)}

def get_oc_installer_properties():

    with open(r"C:\sw\UIM\oc_installer.properties", "a") as pfile:
        for key, value in installer_properties.items():
            # print(key, value)
            # writing all variables into installer.properties file
            pfile.write('{}={}\n'.format(key, value))
    pfile.close()  # closing the file
    time.sleep(5)
    install_operator_console()


def install_operator_console():

    oc_cmd = r"\sw\UIM\oc-installer-20.4.0-windows_x64.exe -i silent -f oc_installer.properties"
    cmd = subprocess.Popen(oc_cmd, shell=True, stderr=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    exit_code = cmd.wait()
    if exit_code == 0:
        print("operator console went Successfully : \n", stdout)
    else:
        print("operator console failed with below error : \n", stderr)


print('Operator Console Installation has taken', (time.time() - start) / 60, 'Minutes..')

get_oc_installer_properties()
