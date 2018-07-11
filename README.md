### Installation
#### Virtual Environment [recommended]
##### Dependencies
```sh
$ sudo apt install python3-venv
```
##### Run venv
```sh
$ . venv/bin/activate
(venv)$ python -V
Python 3.6.5
$ python3 app.py
[?] Install/Update dependencies? Y/n: n
[?] Please enter the name of your wireless interface (for the AP): wlan1
[?] Please enter the name of your internet connected interface: wlan0
[?] Please enter the SSID for the AP: Telefonia2
[?] Please enter the BSSID for the AP: 00:1F:45:7F:DD:1B
[?] Please enter the channel for the AP: 7
```
#### Base OS
```sh
$ pip install -r requirements.txt
$ python3 app.py
```

### Usage

Administrative URL: ```http://127.0.0.1:5000/admin``` ~ ```http://127.0.0.1:5000/users```

![](admin_panel.png)

### Fake Web

URL: ```http://127.0.0.1:5000```

![](fake_web.png)

### IPTABLES

```bash
root@kali:~/github/Fake-CP# iptables -nvL -t nat
Chain PREROUTING (policy ACCEPT 12 packets, 1148 bytes)
 pkts bytes target     prot opt in     out     source               destination
    0     0 DNAT       tcp  --  at0    *       0.0.0.0/0            0.0.0.0/0            tcp dpt:80 to:10.0.0.1:80

Chain INPUT (policy ACCEPT 8 packets, 940 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain OUTPUT (policy ACCEPT 6 packets, 378 bytes)
 pkts bytes target     prot opt in     out     source               destination

Chain POSTROUTING (policy ACCEPT 0 packets, 0 bytes)
 pkts bytes target     prot opt in     out     source               destination
    6   378 MASQUERADE  all  --  *      wlan0   0.0.0.0/0            0.0.0.0/0

```
