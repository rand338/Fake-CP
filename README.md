### Installation
##### Dependencies
```sh
$ sudo apt install python3-venv
```
##### Run on venv [recommended]
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

### Usage

Administrative URL: ```http://127.0.0.1:5000/admin``` ~ ```http://127.0.0.1:5000/users```

![](admin_panel.png)

### Fake Web

URL: ```http://127.0.0.1:5000```

![](fake_web.png)

### IPTables

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
#### Network Interfaces

```bash
root@kali:~/github/Fake-CP# iwconfig
lo        no wireless extensions.

wlan1     IEEE 802.11  Mode:Monitor  Frequency:2.442 GHz  Tx-Power=18 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Power Management:off

eth0      no wireless extensions.

wlan0     IEEE 802.11  ESSID:"Empresa2"
          Mode:Managed  Frequency:2.442 GHz  Access Point: 00:1F:45:7F:DD:18
          Bit Rate=65 Mb/s   Tx-Power=31 dBm
          Retry short limit:7   RTS thr:off   Fragment thr:off
          Encryption key:off
          Power Management:on
          Link Quality=35/70  Signal level=-75 dBm
          Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
          Tx excessive retries:192  Invalid misc:0   Missed beacon:0

at0       no wireless extensions.

```
