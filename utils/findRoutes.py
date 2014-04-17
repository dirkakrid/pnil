#!/usr/bin/env python


import re
import shlex

# ----------------------------------------------------------------
# GLOBAL VARIABLES /REGEXs
# ----------------------------------------------------------------

# FOR IOS / ARISTA
PROTOCOL_RE = re.compile(r'(?<=\s)(([\w])|([\w]\s[\w]+[\d]?)|([\w]+?\*))(?=\s+[\d]+\.)', re.I)
PREFIX_RE = re.compile(r'(([\d]{1,3}\.){3}([\d]{1,3}){1}((/[\d]{1,2})?)((?=\s?\[)|(?=\sis)))', re.I)
# -----------------

# FOR NX-OS DEVICES
PREFIX_NX_RE = re.compile(r'(([\d]{1,3}\.){3}([\d]{1,3}){1}(/[\d]{1,2}))')
PROTOCOL_NX_RE = re.compile(r'(((\w+-\d{1,5}),\s\w+((\w+)(-\d{1})?)))|direct|local|hsrp|glbp', re.I)
# -----------------

# AD_METRIC WORKS ON IOS/ARISTA AND NX-OS
AD_METRIC_RE = re.compile(r'(?<=\[)([0-9]{1,3}/[0-9]{1,3})(?=\])', re.I)
# ---------------------------------------

# NEXTHOP_IP WORKS ON IOS/ARISTA AND NX-OS
NEXTHOP_IP = re.compile(r'(((?<=[\w]{3}\s)(([\d]{1,3}\.){3}[\d]{1,3})(?=,))|connected)', re.I)
NEXTHOP_INT_RE = re.compile(r'((?<=\d,\s)|(?<=connected,\s))(([\w])+([\d]{1,3})(/?)([\d]{1,3})?(/?)([\d]{1,3})?(/?)([\d]{1,3})?)|Null0', re.IGNORECASE)
# ---------------------------------------


# ----------------------------------------------------------------
# get STANDARD ROUTING INFORMATION
# ----------------------------------------------------------------

class standardRoutes(object):
    """docstring for routingInfo"""
    def __init__(self):
        super(standardRoutes, self).__init__()

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
        ad_metric = []
        for ad in search_list:
            ad_match = AD_METRIC_RE.search(ad)
            if ad_match:
                ad_metric.append(ad_match.group(0))
            else:
                ad_metric.append('0/0')

        return ad_metric

    @classmethod
    def getNextHop(cls, search_list):
        next_hop = []
        for n in search_list:
            # finditer returns an iterator if match is found
            n_match = NEXTHOP_IP.finditer(n)

            if n_match:
                for match in n_match:
                    next_hop.append(match.group())
            else:
                next_hop.append('connected')

        return next_hop

    @classmethod
    def getNextHopInterface(cls, search_list):
        next_hop_int = []
        for n in search_list:
            # finditer returns an iterator if match is found
            n_match = NEXTHOP_INT_RE.finditer(n)

            if n_match:
                for match in n_match:
                    next_hop_int.append(match.group())
            else:
                next_hop_int.append('not set')

        return next_hop_int

    @classmethod
    def createRoutesList(cls, routes):
        # form the list of routes and get rid of unnecessary top lines
        routes_list = routes.splitlines()
        routes_list = routes_list[6:]

        prev_line = None
        position = 0
        for line in routes_list:
            # words = line.split(' ')
            words = shlex.split(line)
            len_words = len(words)
            if len_words < 6:
                if prev_line:
                    routes_list[position - 1] = ' '.join([prev_line, line])
                    routes_list[position] = ''

                position += 1
                prev_line = line
                len_words = 0
                words = None
            else:
                prev_line = line
                len_words = 0
                position += 1
                words = None

        return routes_list

    @classmethod
    def getRoutes(cls, routes):
        routes_list = cls.createRoutesList(routes)

        p_keys = cls.getRoutesProtocol(routes_list)
        routes_dict = {key: {} for key in p_keys}

        for line in routes_list:
            p_key = cls.getRoutesProtocol([line])
            prefix = cls.getRoutePrefixes([line])

            # if p_match and pr_match:
            if p_key and prefix:
                ad_metric = cls.getADMetric([line])
                next_hop = cls.getNextHop([line])
                next_hop_int = cls.getNextHopInterface([line])
                routes_dict[p_key[0]][prefix[0]] = {'ad_metric': ad_metric[0],
                                                        'next_hop': next_hop,
                                                        'next_hop_int': next_hop_int
                                            }

        return routes_dict

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# get NX-OS ROUTING INFORMATION
# ----------------------------------------------------------------

class NXOSRoutes(standardRoutes):
    """docstring for NXOSRoutes"""
    def __init__(self):
        super(NXOSRoutes, self).__init__()
