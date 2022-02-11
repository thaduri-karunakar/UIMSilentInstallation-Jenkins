import subprocess
import os
import requests
import time
import zipfile
start = time.time()


url_to_download = [os.getenv("uim_url"), os.getenv("oc_url")]
installer_filename = []
installer_path = r"C:\sw\workspace\\"
deletedir = []
headers = {"X-JFrog-Art-Api": "AKCp8kqgRFpR8hYKGXWiRPW7m2dDrCbsLrWzgeRfUzqiwHEWF55qKFLv2RHvtZWL67dMX8Ad5"}


def download_installers(app_url):
    download = requests.get(app_url, headers=headers, allow_redirects=True, stream=True)
    global  filename
    filename = app_url[app_url.rfind('/')+1:]
    ''' giving exact path to download filename i.e; C:\sw\workspace\niminstall_uimserver_*.zip '''
    filename = installer_path+filename
    # print(filename)
    if "zip" in filename:
        installer_filename.append(filename)
        # print(download.headers)
    with open(filename, 'wb') as f:
        print("downloading ", filename, "...")
        for chunk in download.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    f.close()
    print("{} file download completed ...".format(filename))
    time.sleep(5)





def unzip_installer(uim_file):
    try:

        print("Extracting file : {}".format(uim_file))
        with zipfile.ZipFile(uim_file, "r") as zip_ref:
            global extarct_uim_file
            extarct_uim_file=uim_file.rstrip(".zip")
            deletedir.extend([extarct_uim_file, extarct_uim_file+".zip"])  #deletedir will use while deleting installer directories
            zip_ref.extractall(extarct_uim_file)
            print("{} unzip is done ..".format(extarct_uim_file))

        zip_ref.close()
    except FileNotFoundError as e:
        print("exception is :",e)


def move_installers():
    find_path = r'''dir /S /P "{}\*.exe"'''.format(extarct_uim_file)
    # print("found installer path is :", find_path)
    cmd = subprocess.Popen(find_path, shell=True, stderr=subprocess.PIPE, universal_newlines=True, stdout=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    exit_code = cmd.wait()
    if exit_code == 0:
        path = stdout[stdout.find("C:") - 1:].splitlines()[0]
        print("UIM Installer path is : ", path)
        ''' Move installers from sub directory to root directory'''
        movecmd = '''move /-y {}\* {}"'''.format(path,installer_path)
        cmd = subprocess.Popen(movecmd, shell=True, stderr=subprocess.PIPE, universal_newlines=True,
                               stdout=subprocess.PIPE)
        stdout, stderr = cmd.communicate()
        exit_code = cmd.wait()
        if exit_code == 0:
            pass
            print("UIM Installers moved successfully to : {}".format(installer_path))
            ''' deleting directory '''
            for deletedirfile in deletedir:
                delete_dir = "echo y | del /s {}".format(deletedirfile)
                print("Deleting directory : {}".format(delete_dir))
                cmd = subprocess.Popen(delete_dir, shell=True, stderr=subprocess.PIPE, universal_newlines=True,
                                    stdout=subprocess.PIPE)
                stdout, stderr = cmd.communicate()
                exit_code = cmd.wait()
                if exit_code == 0:
                    print("{} deleted successfully : ".format(delete_dir))
                else:
                    print("failed to delete with fowlloing error :  ", delete_dir, stderr)

        else:
            print("UIM Installers move failed with below error : \n", stderr)
    else:
        print("Failed to find installer path : \n", stderr)



for download_url in url_to_download:
        download_installers(download_url)

for extract_zip in installer_filename:
        unzip_installer(extract_zip)
move_installers()
print('UIM installer has took', (time.time() - start) / 60, 'Minutes..')
