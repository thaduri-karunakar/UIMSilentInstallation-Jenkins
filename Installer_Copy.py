import subprocess
import sys
import time
import traceback
import os

start = time.time()
fileShareIP = os.getenv("fileShareIP").strip()
fileSharePassword = os.getenv("fileSharePassword").strip()
hostName = os.getenv("fileshareHostName").strip()
fileShareUserName = os.getenv("fileShareUserName").strip()
uimVersion = os.getenv("uimVersion").strip()
uim_installer_location = 'C:\sw\\UIM'

netusecmd = r"net use \\{}\C$\sw {} /user:{}\{}".format(fileShareIP, fileSharePassword, hostName, fileShareUserName)


def archive_pkg_copying():
    """ copying packages from LVFILESHARE.dhcp.broadcom.net to UIM server machine"""
    try:
        print("copying UIM and OC Installer packages from renbdl754837-01.bpc.broadcom.net to UIM server machine")
        print(netusecmd)
        cmd = subprocess.Popen(netusecmd, stderr=subprocess.PIPE, shell= True, universal_newlines=True, stdout=subprocess.PIPE)
        stdout, stderr = cmd.communicate()
        exit_code = cmd.wait()

        if exit_code == 0:
            print('net use command executed successfully : ', stdout)
            archive_pkg_copy_cmd = r"echo All | copy \\{}\C$\sw\{}\windows\* {}".format(fileShareIP, uimVersion, uim_installer_location)
            print(archive_pkg_copy_cmd)
            cmd = subprocess.Popen(archive_pkg_copy_cmd, shell= True, stderr=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)
            stdout, stderr = cmd.communicate()
            exit_code = cmd.wait()
            # print(exit_code)
            if exit_code == 0:
                print('UIM installer copy command executed successfully...\n', stdout)
                time.sleep(5)
                print('UIM installer copy has took', (time.time() - start) / 60, 'Minutes..')
            else:
                print('Failed to execute UIM installer copy command  :  {}\n{} '.format(stderr, archive_pkg_copy_cmd))
                print("Exit from the program with above issue...")
                print('UIM installer copy has took', (time.time() - start) / 60, 'Minutes..')
                sys.exit(1)

        else:
            print('Failed to execute net use command :  {}.......\n {} '.format(stderr, stdout))
            print("Exit from the program with above issue...")
            print('UIM installer copy has took', (time.time() - start) / 60, 'Minutes..')
            sys.exit(1)

    except Exception as e:
        print('Below exception occurred')
        traceback.print_exc()


archive_pkg_copying()