#!/usr/bin/env python

import argparse

# ----------------------------------------------------------------
# GLOBAL VARIABLES
# ----------------------------------------------------------------

SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB'],
            1024: ['KB', 'MB', 'GB', 'TB']}

# ----------------------------------------------------------------

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

    parser.add_argument('-f', '--function', help='i.e. -f getHostname, getVersion...')
    parser.add_argument('-c', '--cli', help='i.e. pass a raw cli command')
    parser.add_argument('--vrf', help='Pass a VRF name to the function/cli')
    parser.add_argument('-i', '--ip_address', help='i.e. -i "192.168.31.21"')
    parser.add_argument('-d', '--dns_name', help='i.e. -h sw01.domain.com')
    parser.add_argument('-u', '--username', help='Enter username of device')
    parser.add_argument('-p', '--password', help='Enter password for username')
    parser.add_argument('-n', '--name', help='Enter the device\'s name. i.e -n sw1')
    parser.add_argument('-m', '--manufacturer', help='Enter the manufacturer to run on\
        i.e => -m arista')
    parser.add_argument('-o', '--options', help='Enter an option such as when running\
        "show ip route ospf|bgp"')
    return vars(parser.parse_args())
    


def convertSize(size, suffix, kilobyte_1024_bytes=True):
    '''
    Convert a file size to human-readable form.

    Keyword arguments:
    size                                     --      file size in bytes
    suffix                                  --      suffix to use for calculation, i.e: KB, GiB
    kilobyte_1024_bytes         --      if True (default), use multiples of 1024
                                                          if False, use multiples of 1000

    Returns: string

    '''

    if size < 0:
        raise ValueError('number must be non-negative')

    multiple = 1024 if kilobyte_1024_bytes else 1000
    exponent = SUFFIXES[multiple].index(suffix)
    
    size /= (multiple ** exponent)
    
    return '{0:.1f} {1}'.format(size, suffix)
