#!/usr/bin/env python


# function to check for correct IP Address Input
# this function can later be part of  a larger check_input.py or similar
def checkIP(ip_address):
    ''' Checks a given ipAddress for validity (first octect only for now)'''
    lip = ip_address.split('.')
    if int(lip[0]) <= 0 or int(lip[0]) > 223:
        raise ValueError('Invalid IP')

    return ip_address
