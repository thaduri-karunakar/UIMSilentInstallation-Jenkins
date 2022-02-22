#!/usr/bin/env python
import subprocess
import platform
def get_hostname():
    cmd = subprocess.Popen(['hostname'], stderr=subprocess.PIPE,universal_newlines=True, stdout=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    exit_code = cmd.wait()
    return (stdout).strip()

def get_ip():
    os_type =platform.system()
    return windows_ip() if os_type == 'Windows' else  linux_ip() if os_type == 'Linux' else print(
        'Notable to identify os name by "platform.system()" : {}'.format(os_type))


def windows_ip():
    cmd = subprocess.Popen(['ipconfig'], stderr=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    exit_code = cmd.wait()
    for line in stdout.splitlines():
        if line.strip().startswith('IPv4 Address'):
            # print("The IPV4 Address is : ",line.split(':')[1])
            return (line.split(':')[1]).strip()

def linux_ip():
    cmd = subprocess.run(['ping {}'.format(get_hostname())], stderr=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    exit_code = cmd.wait()
    for line in stdout.splitlines():
        if line.strip().startswith('PING'):
            # print("The IPV4 Address is : ",(line.split(' ')[3]))
            return ((line.split(' ')[3]).strip('()'))


get_hostname()
get_ip()
