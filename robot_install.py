import platform
import subprocess
import  os
import sys
import traceback
import time
import get_hostName_ip
import uim_domain_details

start = time.time()
# uim_ip = "lvntest021804.bpc.broadcom.net"     # UIM Ip will get from jenkins job and will use in uim_domain_details.py
uim_vm_username = os.getenv("uim_vm_username")
uim_vm_password = os.getenv("uim_vm_password")
# uim_hostname = uim_ip.split(".")[0]
os_type = platform.system()
robot_ip = get_hostName_ip.get_ip()
robot_name = get_hostName_ip.get_hostname()

uim_domain_details = uim_domain_details.get_uim_domain_details() #reading uim domain deatils  from uim_domain_details.py --> get_uim_domain_details
print(uim_domain_details)
uim_path = uim_domain_details["address"]
print(uim_path)
nms_robot_variable = {"robotname": robot_name, "hubip": uim_domain_details["ip"], "hubrobotname": uim_domain_details["robot"],
                      "hub": uim_domain_details["hub"], "domain": uim_domain_details["domain"], "robotip": robot_ip, "hubport": os.getenv("hubport")}
def download_windows_robot():
    try:
        netusecmd = r"net use \\{}\C$\PROGRA~1\Nimsoft {} /user:{}\{}".format(uim_domain_details["ip"], uim_vm_password, uim_domain_details["robot"], uim_vm_username)
        cmd = subprocess.Popen(netusecmd, stderr=subprocess.PIPE, shell=True, universal_newlines=True,
                               stdout=subprocess.PIPE)
        stdout, stderr = cmd.communicate()
        exit_code = cmd.wait()
        if exit_code == 0:
            print("net use command executed successfully for windows robot nimsoft-robot-x64.exe")
            robot_installer_copy_cmd = r"echo All | copy \\{}\C$\PROGRA~1\Nimsoft\install\setup\nimsoft-robot-x64.exe C:\sw\Jenkins-slave\workspace".format(uim_ip)
            print(robot_installer_copy_cmd)
            cmd = subprocess.Popen(robot_installer_copy_cmd, shell=True, stderr=subprocess.PIPE, universal_newlines=True,
                                   stdout=subprocess.PIPE)
            stdout, stderr = cmd.communicate()
            exit_code = cmd.wait()
            # print(exit_code)
            if exit_code == 0:
                print('robot installer nimsoft-robot-x64.exe copied successfully...\n')
                time.sleep(1)
                windows_security_certificate_file()
            else:
                print('Failed to execute robot installer nimsoft-robot-x64.exe copy command  :  {}\n{} '.format(stderr, robot_installer_copy_cmd))
                print("Exit from the program with above issue...")
                sys.exit(1)

        else:
            print('Failed to execute net use command :  {}.......\n {} '.format(stderr, stdout))
            print("Exit from the program with above issue...")
            sys.exit(1)
    except Exception as e:
        print('Below exception occurred')
        traceback.print_exc()

def download_linux_robot():
    '''Yet to implement logic...'''

def windows_security_certificate_file():
    try:
        print("Trying to execute security certificate file copy command ...")
        certificate_copy_cmd = r"echo All | Xcopy /E /I \\{}\C$\PROGRA~1\Nimsoft\security C:\sw\Jenkins-slave\security".format(uim_ip)
        print(certificate_copy_cmd)
        cmd= subprocess.Popen(certificate_copy_cmd, shell=True, stderr=subprocess.PIPE, universal_newlines=True,
                                       stdout=subprocess.PIPE)
        stdout, stderr = cmd.communicate()
        exit_code = cmd.wait()
        # print(exit_code)
        if exit_code == 0:
            print('security certificate file copy command executed successfully ...\n')
            time.sleep(1)
        else:
            print('Failed to execute security certificate file copy command  :  {}\n{} '.format(stderr, certificate_copy_cmd))
            print("Exit from the program with above issue...")
            sys.exit(1)
    except Exception as e:
        print('Below exception occurred')
        traceback.print_exc()

def  windows_robot_install():
    with open(r"C:\sw\Jenkins-slave\workspace\nms-robot-vars.cfg", "a") as pfile:
        for key, value in nms_robot_variable.items():
            # print(key, value)
            # writing all variables into installer.properties file
            pfile.write('{}={}\n'.format(key, value))
    pfile.close()  # closing the file
    time.sleep(5)

    robot_install_cmd = r'''\sw\Jenkins-slave\workspace\nimsoft-robot-x64.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART /LOG="robot-log.txt"'''
    cmd = subprocess.Popen(robot_install_cmd, shell=True, stderr=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    exit_code = cmd.wait()
    if exit_code == 0:
        print("robot installation is Successfully completed : \n", stdout)
    else:
        print("robot installation is failed with below error : \n", stderr)

download_windows_robot() if os_type == 'Windows' else download_linux_robot() if os_type == 'Linux' else print(
    'Notable to identify os name by "platform.system()" : {}'.format(os_type))



print('Copying of robot installer has took', (time.time() - start) / 60, 'Minutes..')