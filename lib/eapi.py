#!/usr/bin/env python

# ----------------------------------------------------------------

''' Library to make Arista Networks eAPI calls, furthur documenttion later '''

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Import Server JSON RPC library
# ----------------------------------------------------------------

from jsonrpclib import Server
import re

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Configuration section
# ----------------------------------------------------------------
# _host = "IP address of Arista Switch"
# _api_call ==> Enter the CLI command to run
# _user = '_user with api/admin access'
# _pass = '_pass'
# ----------------------------------------------------------------

class eapi(object):
    """docstring for arista"""
    def __init__(self):
        super(eapi, self).__init__()
        self._host = None
        self._user = 'admin'
        self._pass = 'arista'
        self._switch = None
        self._name = None
        self._version_info = None
        self._connected = False

    def __str__(self):
        rtr_str = 'name:\t\t{0}\nhost:\t\t{1}\nfunction:\t{2}'.format(self._name, self._host)
        return rtr_str

    # ----------------------------------------------------------------
    # "Private / Protected" Methods
    # ----------------------------------------------------------------

    def _connectToSwitch(self):
        try:
            return Server('https://{0}:{1}@{2}/command-api'.format(self._user, self._pass, self._host))
        except Exception as e:
            print ('There was an error trying to connect: {}'.format(e))

    # run CMD
    def _runCmd(self, cli):
        if self._connected:
            return self._switch.runCmds(1, cli)
        else:
            self.connect()
            return self._switch.runCmds(1, cli)

    # run non JSON CMD
    def _runCmdText(self, cli):
        if self._connected:
            return self._switch.runCmds(1, cli, 'text')
        else:
            self.connect()
            return self._switch.runCmds(1, cli, 'text')

    def _versionList(self):
        '''
            Gets version and converts to a list of Ivalues
            this allows comparisons between software versions
            by calling int(on an index)
        '''

        # checks if self._version_info is not empy
        if not self._version_info:
            self.getVersionInfo()

        version_list = self._version_info['version'].split('.')
        return version_list

    @classmethod
    def _createDataDict(cls, key, value):
        return {key: value}

    # ----------------------------------------------------------------
    # Public / Unprotected Methods
    # ----------------------------------------------------------------

    # creates connection to switch
    def connect(self):
        try:
            self._switch = self._connectToSwitch()
            self._connected = True
            return self._switch
        except Exception as e:
            print ('Could not connect, error: {0}'.format(e))

    def setLogin(self, username, password):
        self._user, self._pass = username, password

    def initialize(self, host, name):
        self._host = host
        self._name = name

    def getHost(self):
        return self._createDataDict('host', self._host)

    def getName(self):
        return self._createDataDict('name', self._name)

    # getVersionInfo created to streamline the calling of "show version"
    # there was allot of code that repeated it, this way, only one call is needed
    # speeds up the process and makes it more efficient.
    def getVersionInfo(self):
        ''' returns a 'show version' output as a dictionary '''

        # normaly returns list with dictionary.
        version_info = self._runCmd(['show version'])
        self._version_info = version_info[0]

        #returns only dict of relevant information
        return self._version_info

    def getVersion(self):
        ''' Returns the device running code version as a string '''

        # checks if self._version_info is not empy
        if not self._version_info:
            self.getVersionInfo()

        return self._createDataDict('version', self._version_info['version'])

    # function returns a dictionary of the interfaces and their status
    def getInterfacesStatus(self):
        response = self._runCmd(['show interfaces status'])[0]['interfaceStatuses']

        return response

    def getPlatform(self):
        if not self._version_info:
            self.getVersionInfo()

        return self._createDataDict('platform', self._version_info['modelName'])

    def getSerialNumber(self):

        if not self._version_info:
            self.getVersionInfo()

        serial = self._version_info['serialNumber']

        serial_number = self._createDataDict('serial_number', serial)

        if serial_number['serial_number'] == '':
            non_serial = {'serial_number': 'not_found'}
            return non_serial
        else:
            return serial_number

    def getUptime(self):
        output = self._runCmdText(['show uptime'])[0]['output']
        # finds uptime if output is in H:M or (|) in "number Mins|Days"
        uptime = re.search(r"(?<=up\s)([\d:]+(?=\s?,)) | (?<=up\s)[\d]+\s\w+(?=\s?\,)", output).group(0)
        return self._createDataDict('uptime', uptime)

    def getCPU(self):
        output = self._runCmdText(['show processes top once'])[0]['output']
        
        cpu = re.search(r"\d+\.\d*%(?=us)", output).group(0)
        return self._createDataDict('cpu_usage', cpu)

    def getHostname(self):
        ''' Returns the device's none FQDN hostname '''

        version_int = self._versionList()

        if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
            output = self._runCmd(['show hostname'])[0]['hostname']
            return self._createDataDict('hostname', output)
        else:
            output = self._runCmdText(['show lldp local-info'])[0]['output']

            host = re.search(r"(?<=System Name: \").*?(?=\.)", output).group(0)
            return self._createDataDict('hostname', host)

    def getFQDN(self):
        '''
            Returns the device's FQDN hostname.domain.suffix
            has not been added to main.py yet, waiting to make sure
            their's support accross platforms
        '''

        version_int = self._versionList()

        if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
            output = self._runCmd(["show hostname"])[0]['fqdn']
            return self._createDataDict('fqdn', output)
        else:
            output = self._runCmdText(['show lldp local-info'])[0]['output']

            fqdn = re.search(r"(?<=System Name: \").*?(?=\")", output).group(0)
            return self._createDataDict('fqdn', fqdn)

    def getAAA(self):
        aaa = self._runCmd(['enable', 'show aaa'])[1]['users']
        return aaa

    def getFreeMem(self):

        # checks if self._version_info is not empy
        if not self._version_info:
            self.getVersionInfo()

        free_mem = {'free_memory': self._version_info['memFree']}

        return free_mem

    def getTotalMem(self):

        # checks if self._version_info is not empy
        if not self._version_info:
            self.getVersionInfo()

        total_mem = {'total_memory': self._version_info['memTotal']}

        return total_mem

    def getSystemMac(self):
        if not self._version_info:
            self.getVersionInfo()

        return self._createDataDict('system_mac', self._version_info['systemMacAddress'])

    # ----------------------------------------------------------------
    # FIND ROUTING INFORMATION
    # ----------------------------------------------------------------

    @classmethod
    def getRoutingProtocols(cls, search_list):
        # regEX explination in regex_notes.md
        p_compile = re.compile(r'(?<=\s)((\w)|(\w\s\w+\d?)|(\w+?\*))(?=\s+\d+\.)')

        protocols = []
        for p in search_list:
            p_match = p_compile.search(p)

            if p_match:
                protocols.append(p_match.group(0))

        # removes duplicates from the list, by converting to a set, then back to list
        protocols = list(set(protocols))

        return protocols

    @classmethod
    def getRoutePrefixes(cls, search_list):
        # regEX explination in regex_notes.md
        rp_compile = re.compile(r'((\d{1,3}\.){3}(\d{1,3}){1}(/\d{1,2})|(\d{1,3}\.){3}(\d{1,3}){1}(?=\s?\[))')

        prefixes = []
        for p in search_list:
            pr_match = rp_compile.search(p)
            if pr_match:
                prefixes.append(pr_match.group(0))

        return prefixes

    def getRoutesPerProtocol(self, vrf=None):
        if vrf:
            routes = self._runCmdText(['show ip route vrf {0}'.format(vrf)])[0]['output']
        else:
            routes = self._runCmdText(['show ip route'])[0]['output'].split('\n')

        p_keys = self.getRoutingProtocols(routes)
        pr_keys = self.getRoutePrefixes(routes)
        protocols = {key: {} for key in p_keys}

        # regEX explination in regex_notes.md
        # p_compile = re.compile(r'(?<=\s)((\w)|(\w\s\w+\d?)|(\w+?\*))(?=\s+\d+\.)')

        # regEX explination in regex_notes.md
        # rp_compile = re.compile(r'((\d{1,3}\.){3}(\d{1,3}){1}(/\d{1,2})|(\d{1,3}\.){3}(\d{1,3}){1}(?=\s?\[))')
        # for p in routes:
        #     p_match = p_compile.search(p)
        #     pr_match = rp_compile.search(p)

        #     if p_match and pr_match:
        #         protocols[p_match.group(0)].append(pr_match.group(0))

        # route_info = {}
        # route_info.update(protocols)

        # return route_info
        return protocols

    def getRoutesDetail(self, vrf=None):
        if vrf:
            routes = self._runCmdText(['show ip route vrf {0}'.format(vrf)])[0]['output']
        else:
            routes = self._runCmdText(['show ip route'])[0]['output'].split('\n')
        
        routes = routes[9:-2]

        protocols = [[] for i in range(len(routes))]

        # regEX explination in regex_notes.md
        p_compile = re.compile(r'(?<=\s)((\w)|(\w\s\w+\d?)|(\w+?\*))(?=\s+\d+\.)')

        # regEX explination in regex_notes.md
        rp_compile = re.compile(r'((\d{1,3}\.){3}(\d{1,3}){1}(/\d{1,2})|(\d{1,3}\.){3}(\d{1,3}){1}(?=\s?\[))')
        counter = 0
        for p in routes:
            p_match = p_compile.search(p)
            pr_match = rp_compile.search(p)

            if p_match and pr_match:
                protocols[counter].append(p_match.group(0))
                protocols[counter].append(pr_match.group(0))

                counter += 1

        route_info = {'Routes': []}
        route_info['Routes'] = protocols

        return route_info

    # ----------------------------------------------------------------

    def getDetails(self):

        # moved getVersionInfo() so this information gets refreshed as well
        # and to remove the redundancy of __init__
        self.getVersionInfo()

        items = (
            self.getVersion(),
            self.getCPU(),
            self.getFreeMem(),
            self.getTotalMem(),
            self.getUptime(),
            self.getPlatform(),
            self.getSerialNumber(),
            self.getHost(),
            self.getHostname(),
            self.getName(),
            self.getSystemMac()
            )

        details = {}

        for item in items:
            details.update(item)

        # details = {'hostname': hostname, 'connect_ip': connect_ip, 'platform': platform,
        #               'version': sh_ver, 'serial_number': serial_number, 'system_uptime': uptime,
        #               'cpu_utilization': cpu_utilization, 'free_system_memory': free_memory,
        #               'total_sytem_memory': total_memory, 'vendor': 'arista'}

        return details
