# Custom VPN server using GCP Compute Engine and [PiVPN](http://www.pivpn.io/)

- Many networks block VPN services by filtering traffic by protocol, port or both
- For example, public libraries might block all [UDP](https://en.wikipedia.org/wiki/User_Datagram_Protocol) traffic, or all traffic not using ports 80 (http) or 443 (https)
- Because many third party VPN services use some combination of resources blocked above, one way to improve privacy on public networks is to run a custom VPN server in the cloud
- Typical monthly charge for the setup below as of 10/2018 is < $20 for 100GB of traffic and 24/7 usage

## Requirements:
- This tutorial was written for macOS but works on Linux and Windows with minimal modifications such as proper adjustments to folder locations: 
    - macOS and Linux: ~/Desktop
    - Windows: c:\Users\(username)\Desktop
- Instal Python 3.6+
- Install [GCP SDK](https://cloud.google.com/sdk/)

## 1) Login to [GCP console](https://console.cloud.google.com) and create a Compute Engine instance

- Machine type: *small* (even *micro* is "good enough" in some cases)
- Region and zone: select the closest location to your physical location
- Check *allow https traffic*
- Recommended: use a *pre-emptible* instance to lower charges
- In GCP console, go to VPC network > External IP addresses > switch the type of your instance IP from "Ephemeral" to "Static". This will be your public IP

## 2) Create instance.ini file of the following form and save in the same folder as gcloud.py:

        [dev]
        project = replace_with_gcp_project
        zone = replace_with_instance_zone
        instance_id = replace_with_instance_id
        user = replace_with_user
        gcloud_cmd = replace_with_gcloud_command_typically_gcloud

## 3) Create PiVPN instance

        >> python gcloud.py
        >> ssh
        >> curl -L https://install.pivpn.io | bash

Follow all steps using default values except ports and protocol. Select port 443 and protocol TCP. Select reboot at the end of instalation.

Check if server is working. Enter the commands below. Ports 22 and 443 should be open .

        >> python gcloud.py
        >> ssh
        >> nmap your-public-ip-from-step-1

## 4) Create VPN credentials

        >> pivpn add

Select any name and password and exit from cloud instance

        >> exit

## 5) Save VPN credentials to local computer

        >> python gcloud.py
        >> 3
        >> enter remote folder: typically ~/ovpns
        >> enter local folder: typically ~/Desktop

## 6) Download a VPN client for your platform, add credentials and connect

- macOS example: Download [Tunnelblick](https://tunnelblick.net/) > drag credentials (.ovpn) from previous step to Tunneblick icon > click on Tunneblick icon and connect to your VPN

## 7) Stop GCP instance to prevent charges when VPN is not used. Remember to start GCP instance next time when connecting to your VPN:

        >> python gcloud.py
        >> 2

## Troubleshooting
- Use port 80 above instead of 443
