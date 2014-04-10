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
            return self._switch.runCmds(1, [cli])
        else:
            self.connect()
            return self._switch.runCmds(1, [cli])

    # run non JSON CMD
    def _runCmdText(self, cli):
        if self._connected:
            return self._switch.runCmds(1, [cli], 'text')
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

        version_list = self._version_info['version'].split('.')
        return version_list

    @classmethod
    def _creatDataDict(cls, key, value):
        return {key: value}

    # ----------------------------------------------------------------
    # Public / Unprotected Methods
    # ----------------------------------------------------------------

    # creates connection to switch
    def connect(self):
        self._switch = self._connectToSwitch()
        return self._switch

    def setLogin(self, username, password):
        self._user, self._pass = username, password

    def initialize(self, host, name):
        self._host = host
        self._name = name

    def getHost(self):
        return self._creatDataDict('host', self._host)

    def getName(self):
        return self._creatDataDict('name', self._name)

    # getVersionInfo created to streamline the calling of "show version"
    # there was allot of code that repeated it, this way, only one call is needed
    # speeds up the process and makes it more efficient.
    def getVersionInfo(self):
        ''' returns a 'show version' output as a dictionary '''

        # normaly returns list with dictionary.
        version_info = self._runCmd('show version')
        self._version_info = version_info[0]

        #returns only dict of relevant information
        return self._version_info

    def getVersion(self):
        ''' Returns the device running code version as a string '''

        # checks if self._version_info is not empy
        if not self._version_info:
            self.getVersionInfo()

        return self._creatDataDict('version', self._version_info['version'])

    # function returns a dictionary of the interfaces and their status
    def getInterfaceDetails(self):
        response = self._runCmd('show interfaces status')

        return response[0]['interfaceStatuses']

    def getPlatform(self):
        if not self._version_info:
            self.getVersionInfo()

        return self._creatDataDict('platform', self._version_info['modelName'])

    def getSerialNumber(self):

        if not self._version_info:
            self.getVersionInfo()

        serial = self._version_info['serialNumber']

        serial_number = self._creatDataDict('serial_number', serial)

        if serial_number['serial_number'] == '':
            non_serial = {'serial_number': 'not_found'}
            return non_serial
        else:
            return serial_number

    def getUptime(self):
        output = self._runCmdText('show uptime')
        c = output[0]['output']
        return self._creatDataDict('uptime', c[13:].split(',')[0])

    def getCPU(self):
        output = self._runCmdText('show processes top once')[0]
        
        regex_cpu = re.search(r"\d+\.\d*%(?=us)", output['output'])
        cpu = regex_cpu.group(0)
        return self._creatDataDict('cpu_usage', cpu)

    def getHostname(self):
        ''' Returns the device's none FQDN hostname '''

        version_int = self._versionList()

        if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
            output = self._runCmd('show hostname')
            return self._creatDataDict('hostname', output[0]['hostname'])
        else:
            output = self._runCmdText('show lldp local-info')[0]

            regex_host = re.search(r"(?<=System Name: \").*?(?=\.)", output['output'])
            host = regex_host.group(0)
            return self._creatDataDict('hostname', host)

    def getFQDN(self):
        '''
            Returns the device's FQDN hostname.domain.suffix
            has not been added to main.py yet, waiting to make sure
            their's support accross platforms
        '''

        version_int = self._versionList()

        if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
            output = self._runCmd("show hostname")
            hostname = {'fqdn': output[0]['fqdn']}
            return hostname
        else:
            output = self._runCmdText('show lldp local-info')[0]

            regex_fqdn = re.search(r"(?<=System Name: \").*?(?=\")", output['output'])
            fqdn = regex_fqdn.group(0)
            return self._creatDataDict('fqdn', fqdn)

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

        return self._creatDataDict('system_mac', self._version_info['systemMacAddress'])

    def getDetails(self):

        # moved getVersionInfo() so this information gets refreshed as well
        # and to remove the redundancy of __init__
        self.getVersionInfo()

        # sh_ver = self.getVersion()
        # cpu_utilization = self.getCPU()
        # free_memory = self.getFreeMem()
        # total_memory = self.getTotalMem()
        # uptime = self.getUptime()
        # platform = self.getPlatform()
        # serial_number = self.getSerialNumber()
        # connect_ip = self.getHost()
        # hostname = self.getHostname()

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
