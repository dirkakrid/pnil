#!/usr/bin/env python

# ----------------------------------------------------------------

''' Library to make Arista Networks eAPI calls, furthur documenttion later '''

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Import Server JSON RPC library
# ----------------------------------------------------------------

from jsonrpclib import Server

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
        self._user, self._pass = 'admin', 'arista'
        self._switch = None
        self._version_info = None
        self._connected = False

    # ----------------------------------------------------------------
    # "Private / Protected" Methods
    # ----------------------------------------------------------------

    def _connectToSwitch(self):
        if self._host:
            return Server('https://{0}:{1}@{2}/command-api'.format(self._user, self._pass, self._host))
        else:
            raise ValueError('IP address not set or invalid')

    # run CMD
    def _runCmd(self, cli):
        if self._connected:
            result = self._switch.runCmds(1, [cli])
            self._connected = True
            return result
        else:
            self.connect()
            return self._switch.runCmds(1, [cli])

    # run non JSON CMD
    def _runCmdText(self, cli):
        if self._connected:
            result = self._switch.runCmds(1, [cli], 'text')
            self._connected = True
            return result
        else:
            self.connect()
            return self._switch.runCmds(1, [cli], 'text')

    def _versionList(self):
        '''
            Gets version and converts to a list of Ivalues
            this allows comparisons between software versions
            by calling int(on an index)
        '''

        # checks if self._version_info is not empy
        if not self._version_info:
            self.getVersionInfo()

        version_list = self._version_info[0]['version'].split('.')
        return version_list

    # ----------------------------------------------------------------
    # Public / Unprotected Methods
    # ----------------------------------------------------------------

    # creates connection to switch
    def connect(self):
        self._switch = self._connectToSwitch()
        return self._switch

    def setLogin(self, username, password):
        self._user, self._pass = username, password

    def setHost(self, host):
        self._host = host

    def setAll(self, host, username, password):
        self._host = host
        self._user, self._pass = username, password

    def getHost(self):
        return self._host

    # getVersionInfo created to streamline the calling of "show version"
    # there was allot of code that repeated it, this way, only one call is needed
    # speeds up the process and makes it more efficient.
    def getVersionInfo(self):
        ''' returns a 'show version' output as a dictionary '''

        self._version_info = self._runCmd('show version')
        return self._version_info

    def getVersion(self):
        ''' Returns the device running code version as a string '''

        # checks if self._version_info is not empy
        if not self._version_info:
            self.getVersionInfo()

        return self._version_info[0]['version']

    # function returns a dictionary of the interfaces and their status
    def getIntfStatus(self):
        response = self._runCmd('show interfaces status')

        return response[0]['interfaceStatuses']

    def getPlatform(self):
        if not self._version_info:
            self.getVersionInfo()

        return self._version_info[0]["modelName"]

    def getSerialNumber(self):

        if not self._version_info:
            self.getVersionInfo()

        if self._version_info[0]["serialNumber"] == '':
            return '12345'
        else:
            return self._version_info[0]["serialNumber"]

    def getUptime(self):
        output = self._runCmdText('show uptime')
        c = output[0]['output']
        up_time = c[13:].split(',')[0]
        return up_time

    def getCPU(self):
        output = self._runCmdText('show processes top once')
        # cpu = index 0 of returned list  split by new-lines
        # grabs the 3rd line which contains Cpu values at index [2]
        cpu_line = output[0]['output'].split('\n')[2]

        # cpu is then narrowed down to the actual usage, up to the first instance of a comma ','
        cpu = cpu_line[0:cpu_line.find(',')]
        return cpu

    def getHostname(self):
        ''' Returns the device's none FQDN hostname '''

        version_int = self._versionList()

        if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
            output = self._runCmd('show hostname')
            hostname = output[0]['hostname']
            return hostname
        else:
            # begins a breakdown of finding the hostname inside a string
            # could probably be more efficient, but works for now
            output = self._switch.runCmds(1, ['show lldp local-info'], 'text')

            # gets the 4th line of output which contains the hostname in FQDN format
            host_line = output[0]['output'].split('\n')[3]

            # splits the line into a list at the delimeter and assigns the 2nd indext to fqdn
            # 2nd index contains the hostname
            host_fqdn = host_line.split(':')[1]

            # assignes the first index of fqdn after splitting at the delimeter (.)
            # this splits the fqdn into three parts, the [hostname, domain, suffix]
            hostname = host_fqdn.split('.')[0]

            # indexing removes the " from the begining of the hostname
            return hostname[2:]

    def getFQDN(self):
        '''
            Returns the device's FQDN hostname.domain.suffix
            has not been added to main.py yet, waiting to make sure
            their's support accross platforms
        '''

        version_int = self._versionList()

        if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
            output = self._runCmd("show hostname")
            hostname = output[0]['fqdn']
            return hostname
        else:
            # begins a breakdown of finding the hostname inside a string
            # could probably be more efficient, but works for now
            output = self._switch.runCmds(1, ['show lldp local-info'], 'text')

            # gets the 4th line of output which contains the hostname in FQDN format
            host_line = output[0]['output'].split('\n')[3]

            # splits the line into a list at the delimeter and assigns the 2nd indext to fqdn
            # 2nd index contains the hostname
            hostname = host_line.split(':')[1]

            # indexing removes the quotes (") from the begining and end of the hostname
            return hostname[2:-1]

    def getFreeMem(self):

        # checks if self._version_info is not empy
        if not self._version_info:
            self.getVersionInfo()

        return self._version_info[0]['memFree']

    def getTotalMem(self):

        # checks if self._version_info is not empy
        if not self._version_info:
            self.getVersionInfo()

        return self._version_info[0]['memTotal']

    def getDetails(self):

        # moved getVersionInfo() so this information gets refreshed as well
        # and to remove the redundancy of __init__
        self.getVersionInfo()

        sh_ver = self.getVersion()
        cpu_utilization = self.getCPU()
        free_memory = self.getFreeMem()
        total_memory = self.getTotalMem()
        uptime = self.getUptime()
        platform = self.getPlatform()
        serial_number = self.getSerialNumber()
        connect_ip = self.getHost()
        hostname = self.getHostname()

        details = {'hostname': hostname, 'connect_ip': connect_ip, 'platform': platform,
                      'version': sh_ver, 'serial_number': serial_number, 'system_uptime': uptime,
                      'cpu_utilization': cpu_utilization, 'free_system_memory': free_memory,
                      'total_sytem_memory': total_memory, 'vendor': 'arista'}

        return details
