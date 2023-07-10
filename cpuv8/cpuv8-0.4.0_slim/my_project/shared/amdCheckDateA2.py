#!/bin/env python3

import datetime
from socket import AF_INET, SOCK_DGRAM
import sys
import socket
import struct, time
import os

########################################################################
#                                                                      #
# Licensed per Software License Clickwrap (SPPO).PDF document          #
#                                                                      #
# Copyright 2018-2020 Advanced Micro Devices                           #
#                                                                      #
# PURPOSE: Verifies and corrects the system date.                      #
#                                                                      #
# VERSION: 1.0.0                                                       #
#                                                                      #
########################################################################

def getNTPTime(host = "pool.ntp.org"):
    port = 123
    buf = 1024
    address = (host,port)
    msg = b'\x1b' + 47 * b'\0'

    # reference time (in seconds since 1900-01-01 00:00:00)
    TIME1970 = 2208988800 # 1970-01-01 00:00:00

    # connect to server
    timeout_seconds = 5.0
    time_socket = socket.socket(AF_INET, SOCK_DGRAM)
    max_attempts = 3
    success = False
    for i in range(max_attempts - 1):
        try:
            print("Attempting to get the time from the Internet...")
            time_socket.settimeout(timeout_seconds)
            time_socket.sendto(msg, address)
            time_socket.settimeout(timeout_seconds)
            msg, address = time_socket.recvfrom( buf )
            success = True
            break
        except socket.timeout:
            print("Could not connect to " + host)
            print("Failure " + str(i + 1) + " of " + str(max_attempts) + ".")
            continue
    if not success:
        return None
    t = struct.unpack( "!12I", msg )[10]
    t -= TIME1970

    dt = datetime.datetime.fromtimestamp( t )
    return dt
    #return time.ctime(t).replace("  "," ")

def setCorrectDate():
    CREATION_DATE = datetime.date(2018, 5, 25)
    t = datetime.date.today()
    dt_today = getNTPTime()
    if dt_today is None:
        return None
    os_date = os.popen('date +%m/%d/%Y').read()
    os_date = os_date.strip()
    system_date = t.strftime('%m/%d/%Y')
    print( "datetime.date.today(): " + system_date )
    ntp_date = dt_today.strftime('%m/%d/%Y')
    print( "getNTPTime(): " + ntp_date )
    print( "OS date: " + os_date )
    if os_date == ntp_date:
        print('The system date appears to be correct.')
    else:
        print('The system date appears to be incorrect. Setting date...')
        os.system("date +%m/%d/%Y -s" + dt_today.strftime('%m/%d/%Y') )
        os.system("date +%T -s" + dt_today.strftime('%T') )
    return True

#setCorrectDate()

#print("datetime.date.today() time: " + dt_today.strftime('%T'))
#print(t - dt_today.date())
#print(t.year)