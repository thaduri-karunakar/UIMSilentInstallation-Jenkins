#!/usr/bin/env python
import os
import subprocess
import sys

import get_hostName_ip
import time

start = time.time()
uim_installation_type = os.getenv("uim_installation_type").strip().lower()
# print("uim_installation_type is : ", uim_installation_type)

uim_host_ip = get_hostName_ip.get_ip()
uim_hostname = get_hostName_ip.get_hostname()

fresh_common_variables = ['USER_INSTALL_DIR', 'DB_NORMALIZED_PROVIDER_NAME', 'DB_CREATE_MODE', 'DB_VERSION',
                          'DB_SERVER', 'DB_PORT', 'DB_NAME', 'DB_ADMIN_USERNAME', 'DB_ADMIN_PASSWD', 'NM_ADMIN_PASSWD',
                          'NMS_FIRST_PROBE_PORT', 'WASP_PORT_HTTP', 'TELEMETRY_UPLOAD_OPT_IN_FLAG', 'DB_AUTH_MODE']

upgrade_common_variables = ['NM_ADMIN_PASSWD', 'WASP_PORT_HTTP', 'TELEMETRY_UPLOAD_OPT_IN_FLAG', 'ENABLE_SECURE_BUS',
                            'TUNNEL_PORT', 'CA_CERT_PASSWD', 'CLIENT_CERT_PASSWD']

sqlserver_db_variables = ['DB_ENABLE_TLS', 'DB_TRUST_STORE_PATH', 'DB_TRUST_STORE_PASSWD']

oracle_db_variables = ['DB_SERVICENAME', 'DB_TABLESPACENAME', 'DB_SYS_PASSWD', 'DB_ORACLE_INSTANTCLIENT_DIR',
                       'DB_WALLET_TYPE', 'DB_WALLET_STORE_PATH', 'DB_WALLET_STORE_PASSWD', 'DB_CLIENT_AUTH_NEEDED']

uim_fresh_installer_properties = {"DB_CREATE_MODE": "", "NMS_DOMAIN": "{}_domain".format(uim_hostname),
                                  "DB_VERSION": "", "DB_PORT": "",
                                  "DB_TRUST_STORE_PASSWD": "", "DB_NAME": "", "DB_AUTH_MODE": "",
                                  "DB_SYS_PASSWD": "interOP@123",
                                  "DB_TABLESPACENAME": "", "NMS_PRIMARY_HUB_IP": uim_host_ip,
                                  "NMS_FIRST_PROBE_PORT": "", "ENABLE_SECURE_BUS": "false", "DB_TRUST_STORE_PATH": "",
                                  "DB_ADMIN_PASSWD": "", "NMS_PRIMARY_HUB_NAME": "{}_hub".format(uim_hostname),
                                  "SUPPORT_PASSWD": "mogg10", "TELEMETRY_UPLOAD_OPT_IN_FLAG": "false",
                                  "WASP_PORT_HTTP": "80",
                                  "DB_NORMALIZED_PROVIDER_NAME": "sqlserver", "DB_ADMIN_USERNAME": "sa",
                                  "NM_ADMIN_PASSWD": "interOP@123", "SUPPORT_UNAME": "then@nimsoft.no",
                                  "DB_ENABLE_TLS": "no", "DB_SERVICENAME": "Default", "CLIENT_CERT_PASSWD": "",
                                  "USER_INSTALL_DIR": "", "NMS_PRIMARY_ROBOT_NAME": uim_hostname, "DB_SERVER": "",
                                  "CA_CERT_PASSWD": "", "TUNNEL_PORT": "48003", "DB_ORACLE_INSTANTCLIENT_DIR": "",
                                  "DB_WALLET_TYPE": "", "DB_WALLET_STORE_PATH": "",
                                  "DB_WALLET_STORE_PASSWD": "", "DB_CLIENT_AUTH_NEEDED": ""}

uim_upgrade_installer_properties = {"NM_ADMIN_PASSWD": "", "WASP_PORT_HTTP": "",
                                    "TELEMETRY_UPLOAD_OPT_IN_FLAG": "false", "SUPPORT_UNAME": "", "SUPPORT_PASSWD": "",
                                    "ENABLE_SECURE_BUS": "false", "TUNNEL_PORT": "48003", "CA_CERT_PASSWD": "",
                                    "CLIENT_CERT_PASSWD": ""}


def get_uim_installation_type():
    """Checking UIM installation type (fresh/upgrade)"""
    if uim_installation_type == 'upgrade':
        print('Selected uim_installation_type is : ', uim_installation_type)
        get_uim_upgrade_installer_properties()
    elif uim_installation_type == 'fresh':
        print(' Selected uim_installation_type is : ', uim_installation_type)
        get_uim_fresh_installer_properties()
    elif uim_installation_type not in ['fresh', 'upgrade']:
        print('Provided ENABLE_SECURE_BUS (fresh/upgrade) is not correct, Given input is :', uim_installation_type)
        print("UIM silent installation failed to execute due to invalid user input parameters...")
        exit(1)


def get_uim_fresh_installer_properties():
    """ writing variables into uim_fresh_installer_properties dictionary for fresh scenario """
    for variable in fresh_common_variables:
        user_input = os.getenv("{}".format(variable))
        print(user_input)
        uim_fresh_installer_properties[variable] = user_input
        '''  adding DB specific variables to uim_fresh_installer_properties dictionary  '''
        if uim_fresh_installer_properties['DB_NORMALIZED_PROVIDER_NAME'] == 'sqlserver':
            # print("selected DB_NORMALIZED_PROVIDER_NAME is : ",
            #       uim_fresh_installer_properties['DB_NORMALIZED_PROVIDER_NAME'])
            for sql_variable in sqlserver_db_variables:
                if sql_variable in ["DB_TRUST_STORE_PATH", "DB_TRUST_STORE_PASSWD"]:
                    if uim_fresh_installer_properties["DB_ENABLE_TLS"] == 'yes':
                        sql_user_input = os.getenv("{}".format(sql_variable))
                        print(sql_user_input)
                        uim_fresh_installer_properties[sql_variable] = sql_user_input
                else:
                    sql_user_input = os.getenv("{}".format(sql_variable))
                    print(sql_user_input)
                    uim_fresh_installer_properties[sql_variable] = sql_user_input

        elif uim_fresh_installer_properties['DB_NORMALIZED_PROVIDER_NAME'] == 'oracle':
            print("selected DB_NORMALIZED_PROVIDER_NAME is : ",
                  uim_fresh_installer_properties['DB_NORMALIZED_PROVIDER_NAME'])
            for oracle_variable in oracle_db_variables:
                oracle_user_input = os.getenv("{}".format(oracle_variable)).strip()
                print(oracle_user_input)
                uim_fresh_installer_properties[oracle_variable] = oracle_user_input
    print("Below are the uim_upgrade_installer_properties variables")
    print(uim_fresh_installer_properties)
    # print(uim_fresh_installer_properties['USER_INSTALL_DIR'])
    time.sleep(2)
    print("Calling write_installer_properties_file function to create properties file ...")
    write_installer_properties_file()


def get_uim_upgrade_installer_properties():
    """Writing uim_upgrade_installer_properties variables for upgrade installation"""
    for upgrade_variable in upgrade_common_variables:
        ''' Checking secure bus enabled or not true/false) '''
        if upgrade_variable in ["TUNNEL_PORT", "CA_CERT_PASSWD", "CLIENT_CERT_PASSWD"]:
            if uim_upgrade_installer_properties['ENABLE_SECURE_BUS'] == 'true':
                user_input = os.getenv(upgrade_variable)
                print(user_input)
                uim_upgrade_installer_properties[upgrade_variable] = user_input

            elif uim_upgrade_installer_properties['ENABLE_SECURE_BUS'] not in ['true', 'false']:
                print('Provided ENABLE_SECURE_BUS (true/false) is not correct, Given input is :',
                      uim_upgrade_installer_properties['ENABLE_SECURE_BUS'])
                print("UIM upgrade silent installation failed to execute due to invalid user input parameters...")
                exit(1)

        else:
            user_input = os.getenv(upgrade_variable)
            print(user_input)
            uim_upgrade_installer_properties[upgrade_variable] = user_input
    print("Below are the uim_upgrade_installer_properties variables")
    print(uim_upgrade_installer_properties)
    time.sleep(2)
    print("Calling write_installer_properties_file function to create properties file ...")
    write_installer_properties_file()


def write_installer_properties_file():
    """ creating installer.properties file and writing the variables """
    with open(r"C:\sw\Jenkins\workspace\installer.properties", "a") as pfile:
        print("Writing installer.properties file from uim_{}_installer_properties.items()".
              format(uim_installation_type))
        write_function = "uim_{}_installer_properties.items()".format(uim_installation_type)
        if uim_installation_type == 'fresh':
            for key, value in uim_fresh_installer_properties.items():
                pfile.write('{}={}\n'.format(key, value))  # writing all variables into installer.properties file
        elif uim_installation_type == 'upgrade':
            for key, value in uim_upgrade_installer_properties.items():
                pfile.write('{}={}\n'.format(key, value))  # writing all variables into installer.properties file
    pfile.close()  # closing the file
    time.sleep(5)
    print("Calling install_uim_server function to start silent installation of UIM ...")
    install_uim_server()
    print('UIM installer has took', (time.time() - start) / 60, 'Minutes..')


def install_uim_server():
    uimcmd = r"\sw\Jenkins\workspace\setupCAUIMServer.exe -i silent -f installer.properties"
    cmd = subprocess.Popen(uimcmd, shell=True, stderr=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    exit_code = cmd.wait()
    if exit_code == 0:
        print("UIM Installation went Successfully ... \n", stdout)

        ''' Deploying uimapi probe on primary hub '''

        print("Deploying uimapi probe on primary hub ...")
        probe_deploy = r"C:\Progra~1\Nimsoft\bin\pu -u administrator -p {0} /{1}_domain/{1}_hub/{1}/controller inst_request uimapi".format(os.getenv("NM_ADMIN_PASSWD"),uim_hostname )
        cmd = subprocess.Popen(probe_deploy, shell=True, stderr=subprocess.PIPE, universal_newlines=True,
                               stdout=subprocess.PIPE)
        stdout, stderr = cmd.communicate()
        exit_code = cmd.wait()
        if exit_code == 0:
            print("uimapi package deployed successfully on primary hub ... \n", stdout)
            print("Waiting for 3 minutes for wasp probe to come up ...")
            time.sleep(180)
        else:
            print("Failed to deploy uimapi package ... \n", stderr)
            sys.exit(1)

    else:
        print("UIM Installation failed with below error : \n", stderr)
        sys.exit(1)

get_uim_installation_type()
