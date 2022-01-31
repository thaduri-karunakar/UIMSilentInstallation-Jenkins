#!/usr/bin/env python
import os
import subprocess

import get_hostName_ip
import time
uim_installation_type = os.getenv("uim_installation_type").strip().lower()
print(uim_installation_type)

fresh_common_variables = ['USER_INSTALL_DIR', 'DB_NORMALIZED_PROVIDER_NAME', 'DB_CREATE_MODE', 'DB_VERSION',
                          'DB_SERVER', 'DB_PORT', 'DB_NAME', 'DB_ADMIN_USERNAME', 'DB_ADMIN_PASSWD', 'NM_ADMIN_PASSWD',
                          'NMS_FIRST_PROBE_PORT', 'WASP_PORT_HTTP', 'TELEMETRY_UPLOAD_OPT_IN_FLAG','DB_AUTH_MODE']

upgrade_common_variables = ['NM_ADMIN_PASSWD', 'WASP_PORT_HTTP', 'TELEMETRY_UPLOAD_OPT_IN_FLAG']

sqlserver_db_variables = ['DB_ENABLE_TLS', 'DB_TRUST_STORE_PATH', 'DB_TRUST_STORE_PASSWD']

oracle_db_variables = ['DB_SERVICENAME', 'DB_TABLESPACENAME', 'DB_SYS_PASSWD', 'DB_ORACLE_INSTANTCLIENT_DIR',
                       'DB_WALLET_TYPE', 'DB_WALLET_STORE_PATH', 'DB_WALLET_STORE_PASSWD', 'DB_CLIENT_AUTH_NEEDED']

secure_bus_enabled_variables = ['TUNNEL_PORT', 'CA_CERT_PASSWD', 'CLIENT_CERT_PASSWD']

installer_properties = {"DB_CREATE_MODE": "", "NMS_DOMAIN": "{}_domain".format(get_hostName_ip.get_hostname()), "DB_VERSION": "", "DB_PORT": "",
                        "DB_TRUST_STORE_PASSWD": "", "DB_NAME":"",  "DB_AUTH_MODE":"", "DB_SYS_PASSWD":"",
                        "DB_TABLESPACENAME":"", "NMS_PRIMARY_HUB_IP":get_hostName_ip.get_ip(),
                        "NMS_FIRST_PROBE_PORT":"", "ENABLE_SECURE_BUS":"false", "DB_TRUST_STORE_PATH":"",
                        "DB_ADMIN_PASSWD":"", "NMS_PRIMARY_HUB_NAME":"{}_hub".format(get_hostName_ip.get_hostname()), "SUPPORT_PASSWD":"mogg10", "TELEMETRY_UPLOAD_OPT_IN_FLAG":"false", "WASP_PORT_HTTP":"80",
                        "DB_NORMALIZED_PROVIDER_NAME":"sqlserver", "DB_ADMIN_USERNAME":"sa", "NM_ADMIN_PASSWD":"interOP@123", "SUPPORT_UNAME":"then@nimsoft.no", "DB_ENABLE_TLS":"no", "DB_SERVICENAME":"", "CLIENT_CERT_PASSWD":"",
                        "USER_INSTALL_DIR":"", "NMS_PRIMARY_ROBOT_NAME":get_hostName_ip.get_hostname(), "DB_SERVER":"", "CA_CERT_PASSWD":"", "TUNNEL_PORT":"48003", "DB_ORACLE_INSTANTCLIENT_DIR":"", "DB_WALLET_TYPE":"", "DB_WALLET_STORE_PATH":"",
                        "DB_WALLET_STORE_PASSWD":"", "DB_CLIENT_AUTH_NEEDED":""}


def get_installer_properties():

    # Checking UIM installation type (fresh/upgrade)
    if uim_installation_type == 'upgrade':
        print(' Selected uim_installation_type is : ', uim_installation_type)
        secure_bus_enable_input = str(input("Do you want to enable secure bus (true|false) :  ").strip())
        ''' Writing installer_properties variables for upgrade installation'''
        for upgrade_variable in upgrade_common_variables:
            user_input = input("Provide {} value :  ".format(upgrade_variable)).strip()
            print(user_input)
            # writing variables into installer_properties dictionary for upgrade scenario
            installer_properties[upgrade_variable] = user_input

        ''' Checking secure bus enabled or not true/false) '''
        if secure_bus_enable_input == 'true':
            installer_properties['ENABLE_SECURE_BUS'] = 'true'
            for secure_bus_variable in secure_bus_enabled_variables:
                secure_bus_input = input("Provide {} value :  ".format(secure_bus_variable)).strip()
                print(secure_bus_input)
                installer_properties[secure_bus_variable] = secure_bus_input
            print(installer_properties)
        elif secure_bus_enable_input not in ['true', 'false']:
            print('Provided ENABLE_SECURE_BUS (true/false) is not correct, Given input is :', secure_bus_enable_input)
            exit()

    elif uim_installation_type == 'fresh':
        for variable in fresh_common_variables:
            user_input = os.getenv("{}".format(variable))
            print(user_input)
            # writing variables into installer_properties dictionary for fresh scenario
            installer_properties[variable] = user_input

            '''  adding DB specific variables to installer_properties dictionary  '''

        if installer_properties['DB_NORMALIZED_PROVIDER_NAME'] == 'sqlserver':
            print(installer_properties['DB_NORMALIZED_PROVIDER_NAME'])
            for sql_variable in sqlserver_db_variables:
                if sql_variable in ["DB_TRUST_STORE_PATH","DB_TRUST_STORE_PASSWD"]:
                    if installer_properties["DB_ENABLE_TLS"] == 'yes':
                        sql_user_input = os.getenv("{}".format(sql_variable))
                        print(sql_user_input)
                        installer_properties[sql_variable] = sql_user_input
                else:
                    sql_user_input = os.getenv("{}".format(sql_variable))
                    print(sql_user_input)
                    installer_properties[sql_variable] = sql_user_input
        elif installer_properties['DB_NORMALIZED_PROVIDER_NAME'] == 'oracle':
            print(installer_properties['DB_NORMALIZED_PROVIDER_NAME'])
            for oracle_variable in oracle_db_variables:
                oracle_user_input = os.getenv("{}".format(oracle_variable)).strip()
                print(oracle_user_input)
                installer_properties[oracle_variable] = oracle_user_input

    elif uim_installation_type not in ['fresh', 'upgrade']:
        print('Provided ENABLE_SECURE_BUS (fresh/upgrade) is not correct, Given input is :', uim_installation_type)
        exit()
    print(installer_properties)
    # print(installer_properties['USER_INSTALL_DIR'])
    # creating installer.properties file and writing the variables
    with open(r"C:\sw\UIM\installer.properties", "a+") as pfile:
        for key, value in installer_properties.items():
            # print(key, value)
            # writing all variables into installer.properties file
            pfile.write('{}={}\n'.format(key, value))
    pfile.close()  # closing the file
    time.sleep(5)
    install_uim_server()

def install_uim_server():
    uimCmd = r"\sw\UIM\setupCAUIMServer.exe -i silent -f installer.properties"
    cmd = subprocess.Popen(uimCmd, shell=True, stderr=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    exit_code = cmd.wait()
    if exit_code == 0:
        print("UIM Installation went Successfully : \n", stdout)
    else:
        print("UIM Installation failed with below error : \n", stderr)



get_installer_properties()
