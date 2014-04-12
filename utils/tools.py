#!/usr/bin/env python

import argparse
import re

# ----------------------------------------------------------------
# GLOBAL VARIABLES
# ----------------------------------------------------------------

# regEX explinations in regex_notes.md
PROTOCOL_RE = re.compile(r'(?<=\s)(([a-zA-Z])|([a-zA-Z]\s[a-zA-Z]+[0-9]?)|([a-zA-Z]+?\*))(?=\s+[0-9]+\.)')
PREFIX_RE = re.compile(r'(([0-9]{1,3}\.){3}([0-9]{1,3}){1}((/[0-9]{1,2})?)((?=\s?\[)|(?=\sis)))')
AD_METRIC_RE = re.compile(r'(?<=\[)([0-9]{1,3}/[0-9]{1,3})(?=\])')
NEXTHOP_IP = re.compile(r'(?<=[a-zA-Z]{3}\s)(([0-9]{1,3}\.){3}[0-9]{1,3}(?=,))')
NEXTHOP_INT_RE = re.compile(r'([a-zA-Z])+([0-9]{1,3})(/?)([0-9]{1,3})?(/?)([0-9]{1,3})?(/?)([0-9]{1,3})?$')


SUFFIXES = {1000: ['KB', 'MB', 'GB', 'TB'],
                1024: ['KB', 'MB', 'GB', 'TB']}

# ----------------------------------------------------------------

class utils(object):
    """docstring for utils"""
    def __init__(self):
        super(utils, self).__init__()
        
    # function to check for correct IP Address Input
    # this function can later be part of  a larger check_input.py or similar
    @classmethod
    def checkIP(cls, ip_address):
        ''' Checks a given ipAddress for validity (first octect only for now)'''
        lip = ip_address.split('.')
        if int(lip[0]) <= 0 or int(lip[0]) > 223:
            raise ValueError('Invalid IP')

        return ip_address
    @classmethod
    def initArgs(cls):
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
        args = vars(parser.parse_args())
        return args

    @classmethod
    def convertSize(cls, size, suffix, kilobyte_1024_bytes=True):
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

class routingInfo(object):
    """docstring for routingInfo"""
    def __init__(self):
        super(routingInfo, self).__init__()
    
    # ----------------------------------------------------------------
    # FIND ROUTING INFORMATION
    # ----------------------------------------------------------------

    @classmethod
    def getRoutesProtocol(cls, search_list):
        protocols = []
        for p in search_list:
            p_match = PROTOCOL_RE.search(p)

            if p_match:
                protocols.append(p_match.group(0))

        # removes duplicates from the list, by converting to a set, then back to list
        if len(protocols) > 1:
            protocols = list(set(protocols))

        return protocols

    @classmethod
    def getRoutePrefixes(cls, search_list):
        prefixes = []
        for p in search_list:
            # The test for protocol first in the prefix line is necessary
            # the regEX matching the prefix, sometimes matches an un-necessary line
            # such as 10.0.0.0/8 is variably subneted, under this line, are the actual prefixes
            protocol = cls.getRoutesProtocol([p])
            if protocol:
                pr_match = PREFIX_RE.search(p)
                if pr_match:
                    prefixes.append(pr_match.group(0))

        return prefixes

    @classmethod
    def getADMetric(cls, search_list):
        admetric = []
        for ad in search_list:
            ad_match = AD_METRIC_RE.search(ad)
            if ad_match:
                admetric.append(ad_match.group(0))
            else:
                admetric.append('0/0')

        return admetric

    @classmethod
    def getNextHop(cls, search_list):
        next_hop = []
        for n in search_list:
            n_match = NEXTHOP_IP.search(n)
            if n_match:
                next_hop.append(n_match.group(0))
            else:
                next_hop.append('connected')

        return next_hop

    @classmethod
    def getNextHopInterface(cls, search_list):
        next_hop_int = []
        for n in search_list:
            n_match = NEXTHOP_INT_RE.search(n)
            if n_match:
                next_hop_int.append(n_match.group(0))
            else:
                next_hop_int.append('not set')

        return next_hop_int

    @classmethod
    def getRoutes(cls, routes_list):
        p_keys = cls.getRoutesProtocol(routes_list)
        routes_dict = {key: {} for key in p_keys}

        for p in routes_list:
            p_key = cls.getRoutesProtocol([p])
            prefix = cls.getRoutePrefixes([p])

            # if p_match and pr_match:
            if p_key and prefix:
                ad_metric = cls.getADMetric([p])
                next_hop = cls.getNextHop([p])
                next_hop_int = cls.getNextHopInterface([p])
                routes_dict[p_key[0]][prefix[0]] = {'ad_metric': ad_metric[0],
                                                        'next_hop': next_hop[0],
                                                        'next_hop_int': next_hop_int[0]
                                            }

        return routes_dict

    # ----------------------------------------------------------------


class printRouting(object):
    """docstring for printRouting"""
    def __init__(self):
        super(printRouting, self).__init__()
        
    @classmethod
    def printConnected(cls, result):
        print('\n')
        print ('# CONNECTED ROUTES')
        print('#' + '*' * 80)
        for prefix, values in result['C'].iteritems():
            prefix_tab = '\t\t' if len(prefix) <= 13 else '\t'
            next_tab = '\t\t' if len(values['next_hop']) <= 13 else '\t'
            print ('# Prefix: {0}{1}AD/Metric: {2}\tNext-Hop: {3}{4}Next-Hop-Interface: {5}\
                        '.format(prefix, prefix_tab, values['ad_metric'], values['next_hop'],\
                         next_tab, values['next_hop_int']))

    print('\n')

    @classmethod
    def printStatics(cls, result):
        print('\n')
        print ('# STATIC ROUTES')
        print('#' + '*' * 80)
        for prefix, values in result['S'].iteritems():
            prefix_tab = '\t\t' if len(prefix) <= 13 else '\t'
            next_tab = '\t\t' if len(values['next_hop']) <= 13 else '\t'
            print ('# Prefix: {0}{1}AD/Metric: {2}\tNext-Hop: {3}{4}Next-Hop-Interface: {5}\
                        '.format(prefix, prefix_tab, values['ad_metric'], values['next_hop'],\
                         next_tab, values['next_hop_int']))

        print('\n')

    @classmethod
    def printOSPF(cls, result):
        ospf_keys = ['O', 'O IA', 'O E2', 'O E1', 'O N1', 'O N2']
        print('\n')
        print ('# OSPF ROUTES')
        print('#' + '*' * 80)
        for key in ospf_keys:
            if key in result.keys():
                for prefix, values in result[key].iteritems():
                    prefix_tab = '\t\t' if len(prefix) <= 13 else '\t'
                    next_tab = '\t\t' if len(values['next_hop']) <= 13 else '\t'
                    print ('# Prefix: {0}{1}AD/Metric: {2}\tNext-Hop: {3}{4}Next-Hop-Interface: {5}\
                        '.format(prefix, prefix_tab, values['ad_metric'],\
                            values['next_hop'], next_tab, values['next_hop_int']))

        print('\n')

    @classmethod
    def printBGP(cls, result):
        print('\n')
        print ('# BGP ROUTES')
        print('#' + '*' * 80)
        for prefix, values in result['B'].iteritems():
            prefix_tab = '\t\t' if len(prefix) <= 13 else '\t'
            next_tab = '\t\t' if len(values['next_hop']) <= 13 else '\t'
            print ('# Prefix: {0}{1}AD/Metric: {2}\tNext-Hop: {3}{4}Next-Hop-Interface: {5}\
                        '.format(prefix, prefix_tab, values['ad_metric'], values['next_hop'],\
                         next_tab, values['next_hop_int']))
        print('\n')

    @classmethod
    def findByProtocol(cls, result, protocol='S'):
        if protocol.lower() == 'c' or protocol.lower() == 'connected':
            cls.printConnected(result)
        elif protocol.lower() == 's' or protocol.lower() == 'static':
            cls.printStatics(result)
        elif protocol.lower() == 'o' or protocol.lower() == 'ospf':
            cls.printOSPF(result)
        elif protocol.lower() == 'b' or protocol.lower() == 'bgp':
            cls.printBGP(result)
