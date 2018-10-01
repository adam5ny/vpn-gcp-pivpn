import configparser
import os
import subprocess
import sys

conf = configparser.ConfigParser()
conf.read(os.path.abspath(os.path.join(os.path.dirname( __file__ ), "secrets.ini")))

project = conf["dev"]["project"]
zone = conf["dev"]["zone"]
instance_id = conf["dev"]["instance_id"]
user = conf["dev"]["user"]
gcloud_cmd = conf["dev"]["gcloud_cmd"]

def main():
    print("""
    ssh - ssh into instance {0}
    1 - start instance {0}
    2 - stop instance {0}
    3 - gcloud scp files to local folder
    """.format(instance_id))
    help_str = "Please make selection(s). For multi-selection, separate by ',': "
    selections = [x.strip() for x in input(help_str).split(",")]
    for i in selections:
        if i == "ssh":
            ssh()
        elif i == "1":
            start()
        elif i == "2":
            stop()
        elif i == "3":
            scp_from_gcp_to_desktop()
        else:
            sys.exit("Invalid selection")

def ssh():
    subprocess.call("""
    {3} compute --project {0} ssh --zone {1} {4}@{2}
    """.format(project, zone, instance_id, gcloud_cmd, user), shell=True)

def start():
    subprocess.call("""
    {0} compute instances start {1} --zone {2}
    """.format(gcloud_cmd, instance_id, zone), shell=True)

def stop():
    subprocess.call("""
    {0} compute instances stop {1} --zone {2}
    """.format(gcloud_cmd, instance_id, zone), shell=True)

def scp_from_gcp_to_desktop():
    gcp_folder = input("Enter gcp folder: ")
    local_folder = input("Enter target folder on local machine: ")
    cmd = "{2} compute scp --recurse {3}@{1}:{5} {4} --zone {0};".format(
        zone, instance_id, gcloud_cmd, user, 
        local_folder, gcp_folder)
    subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    main()