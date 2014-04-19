#!/usr/bin/env python


import re
import shlex

# ----------------------------------------------------------------
# GLOBAL VARIABLES /REGEXs
# ----------------------------------------------------------------

# FOR IOS / ARISTA
PROTOCOL_RE = re.compile(r'(?<=\s)(?:([\w])|(?:[\w]\s[\w]+[\d]?)|(?:[\w]+?\*))(?=\s+[\d]+\.)', re.I)
PREFIX_RE = re.compile(r'((?:[\d]{1,3}\.){3}(?:[\d]{1,3}){1}((?:/[\d]{1,2})?)((?=\s?\[)|(?=\sis)))', re.I)
# -----------------

# FOR NX-OS DEVICES
PREFIX_NX_RE = re.compile(r'((?:[\d]{1,3}\.){3}(?:[\d]{1,3}){1}(?:/[\d]{1,2}))')
PROTOCOL_NX_RE = re.compile(r'(((?:\w+-\d{1,5}),\s\w+((?:\w+)(?:-\d{1})?)))|direct|local|hsrp|glbp', re.I)
# -----------------

# AD AND METRIC WORKS ON IOS/ARISTA AND NX-OS
METRIC_RE = re.compile(r'(?<=/)(?:\d{1,7})(?=])', re.I)
ADMIN_DISTANCE_RE = re.compile(r'(?<=\[)(?:\d{1,7})(?=/)')
# ---------------------------------------

# NEXTHOP_IP WORKS ON IOS/ARISTA AND NX-OS
NEXTHOP_IP = re.compile(r'(((?<=[\w]{3}\s)(?:(?:[\d]{1,3}\.){3}[\d]{1,3})(?=,))|connected)', re.I)
NEXTHOP_INT_RE = re.compile(r'((?<=\d,\s)|(?<=connected,\s))((?:[\w])+(?:[\d]{1,3})(?:/?)(?:[\d]{1,3})?(?:/?)(?:[\d]{1,3})?(?:/?)(?:[\d]{1,3})?)|Null0', re.IGNORECASE)
# ---------------------------------------


# ----------------------------------------------------------------
# get STANDARD ROUTING INFORMATION
# ----------------------------------------------------------------

class standardRoutes(object):
    """docstring for routingInfo"""
    def __init__(self):
        super(standardRoutes, self).__init__()

    @classmethod
    def getProtocols(cls, search_list):
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
    def getSingleProtocol(cls, line):
        p_match = PROTOCOL_RE.search(line)
        protocol = p_match.group(0) if p_match else None

        return protocol

    @classmethod
    def getRoutePrefixes(cls, search_list):
        prefixes = []
        for p in search_list:
            # The test for protocol first in the prefix line is necessary
            # the regEX matching the prefix, sometimes matches an un-necessary line
            # such as 10.0.0.0/8 is variably subneted, under this line, are the actual prefixes
            protocol = cls.getSingleProtocol(p)
            prefix = PREFIX_RE.search(p)
            if protocol and prefix:
                prefixes.append(prefix.group(0))

        return prefixes

    @classmethod
    def getSinglePrefix(cls, line):
        pr_match = PREFIX_RE.search(line)
        prefix = pr_match.group(0) if pr_match else None

        return prefix


    @classmethod
    def getAdminDistance(cls, search_list):
        admin_distance = []
        for ad in search_list:
            ad_match = ADMIN_DISTANCE_RE.search(ad)
            if ad_match:
                admin_distance.append(ad_match.group(0))
            else:
                admin_distance.append('0')

        return admin_distance

    @classmethod
    def getMetric(cls, search_list):
        metric = []
        for m in search_list:
            m_match = METRIC_RE.search(m)
            if m_match:
                metric.append(m_match.group(0))
            else:
                metric.append('0')

        return metric

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
        routes_dict = {}

        for line in routes_list:
            protocol = cls.getSingleProtocol(line)
            prefix = cls.getSinglePrefix(line)

            if prefix:
                admin_distance = cls.getAdminDistance([line])
                metric = cls.getMetric([line])
                next_hop = cls.getNextHop([line])
                next_hop_int = cls.getNextHopInterface([line])
                routes_dict[prefix] = {'admin_distance': admin_distance,
                                                    'protocol': protocol,
                                                    'metric': metric,
                                                    'next_hop': next_hop,
                                                    'next_hop_int': next_hop_int}

        return routes_dict

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# get NX-OS ROUTING INFORMATION
# ----------------------------------------------------------------

class NXOSRoutes(standardRoutes):
    """docstring for NXOSRoutes"""
    def __init__(self):
        super(NXOSRoutes, self).__init__()
