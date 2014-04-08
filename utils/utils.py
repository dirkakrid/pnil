#!/usr/bin/env python

import argparse


# function to check for correct IP Address Input
# this function can later be part of  a larger check_input.py or similar
def checkIP(ip_address):
    ''' Checks a given ipAddress for validity (first octect only for now)'''
    lip = ip_address.split('.')
    if int(lip[0]) <= 0 or int(lip[0]) > 223:
        raise ValueError('Invalid IP')

    return ip_address

def initArgs():
    parser = argparse.ArgumentParser(description='\
        input -f [function] -i [ipAddress] \
        -u [username] -p [password]')

    parser.add_argument('-f', '--function', help='i.e. -f showIntfStatus, show version')
    parser.add_argument('-c', '--cli', help='i.e. same as -f, for redundancy')
    parser.add_argument('-i', '--ip_address', help='i.e. -i "192.168.31.21"')
    parser.add_argument('-n', '--host', help='i.e. -h sw01.domain.com')
    parser.add_argument('-u', '--user', help='Enter username of device')
    parser.add_argument('-p', '--pass', help='Enter password for username')
    parser.add_argument('-m', '--manufacturer', help='Enter the manufacturer to run on\
        i.e => -m arista')
    _args = vars(parser.parse_args())
    return _args
