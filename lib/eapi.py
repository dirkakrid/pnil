#!/usr/bin/env python

# Python Network Interface Library
#
# Author:             Yandy Ramirez
# Twitter:             @IPyandy (https://twitter.com/IPyandy)
# Site:                  http://ipyandy.net
# Code Verion:      0.0.1
#
# ----------------------------------------------------------------

'''
 Library to make Arista Networks eAPI calls, furthur documenttion later
 '''

# ----------------------------------------------------------------

from __future__ import print_function
import sys

if sys.version_info > (2, 7, 2) and sys.version_info < (3, 0):
    # ----------------------------------------------------------------
    # Import Server JSON RPC library
    # ----------------------------------------------------------------

    from jsonrpclib import Server
    from pnil.utils.findRoutes import standardRoutes
    import re

    # ----------------------------------------------------------------
    # GLOBAL VARIABLES
    # ----------------------------------------------------------------


    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # Configuration section
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------

    class eapiInfo(object):
        """docstring for eapiInfo"""
        def __init__(self):
            super(eapiInfo, self).__init__()

        def findHost(self):
            return eapi.createDataDict('host', self._host)

        def _versionList(self):
            '''
                finds version and converts to a list of Ivalues
                this allows comparisons between software versions
                by calling int(on an index)
            '''

            # checks if self._version_info is not empy
            if not self._version_info:
                self.findVersionInfo()

            version_list = self._version_info['version'].split('.')
            return version_list

        # findVersionInfo created to streamline the calling of "show version"
        # there was allot of code that repeated it, this way, only one call is needed
        # speeds up the process and makes it more efficient.
        def findVersionInfo(self):
            ''' returns a 'show version' output as a dictionary '''

            # normaly returns list with dictionary.
            version_info = eapi._runCMD(self, ['show version'])
            self._version_info = version_info[0]

            #returns only dict of relevant information
            return self._version_info

        def findName(self):
            return eapi.createDataDict('name', self._name)

        def findVersion(self):
            ''' Returns the device running code version as a string '''

            # checks if self._version_info is not empy
            if not self._version_info:
                self.findVersionInfo()

            return eapi.createDataDict('version', self._version_info['version'])

        # function returns a dictionary of the interfaces and their status
        def findInterfacesStatus(self):
            response = eapi._runCMD(self, ['show interfaces status'])[0]['interfaceStatuses']

            return response

        def findPlatform(self):
            if not self._version_info:
                self.findVersionInfo()

            return eapi.createDataDict('platform', self._version_info['modelName'])

        def findSerialNumber(self):

            if not self._version_info:
                self.findVersionInfo()

            serial = self._version_info['serialNumber']

            serial_number = eapi.createDataDict('serial_number', serial)

            if serial_number['serial_number'] == '':
                non_serial = {'serial_number': 'not_found'}
                return non_serial
            else:
                return serial_number

        def findUptime(self):
            output = eapi._runCMDText(self, ['show uptime'])[0]['output']
            # finds uptime if output is in H:M or (|) in "number Mins|Days"
            up_split = re.split(r"up\s+?", output)

            uptime = re.match(r'(^(\d{1,3}:\d{1,3})|^(\d{1,3})\s\w+)', up_split[1]).group(0)
            return eapi.createDataDict('uptime', uptime)

        def findCPU(self):
            output = eapi._runCMDText(self, ['show processes top once'])[0]['output']
            
            cpu = re.search(r"\d+\.\d*%(?=us)", output).group(0)
            return eapi.createDataDict('cpu_usage', cpu)

        def findHostname(self):
            ''' Returns the device's none FQDN hostname '''

            version_int = self._versionList()

            if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
                output = eapi._runCMD(self, ['show hostname'])[0]['hostname']
                return eapi.createDataDict('hostname', output)
            else:
                output = eapi._runCMDText(self, ['show lldp local-info'])[0]['output']

                host = re.search(r"(?<=System Name: \").*?(?=\.)", output).group(0)
                return eapi.createDataDict('hostname', host)

        def findFQDN(self):
            '''
                Returns the device's FQDN hostname.domain.suffix
                has not been added to main.py yet, waiting to make sure
                their's support accross platforms
            '''

            version_int = self._versionList()

            if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
                output = eapi._runCMD(self, ["show hostname"])[0]['fqdn']
                return eapi.createDataDict('fqdn', output)
            else:
                output = eapi._runCMDText(eapi, ['show lldp local-info'])[0]['output']

                fqdn = re.search(r"(?<=System Name: \").*?(?=\")", output).group(0)
                return eapi.createDataDict('fqdn', fqdn)

        def findAAA(self):
            aaa = eapi._runCMD(self, ['enable', 'show aaa'])[1]['users']
            return aaa

        def findFreeMem(self):

            # checks if self._version_info is not empy
            if not self._version_info:
                self.findVersionInfo()

            return eapi.createDataDict('free_memory', self._version_info['memFree'])

        def findTotalMem(self):

            # checks if self._version_info is not empy
            if not self._version_info:
                self.findVersionInfo()

            return eapi.createDataDict('total_memory', self._version_info['memTotal'])

        def findSystemMac(self):
            if not self._version_info:
                self.findVersionInfo()

            return eapi.createDataDict('system_mac', self._version_info['systemMacAddress'])


        def findDetails(self):

            # moved findVersionInfo() so this information finds refreshed as well
            # and to remove the redundancy of __init__
            self.findVersionInfo()

            items = (
                self.findVersion(),
                self.findCPU(),
                self.findFreeMem(),
                self.findTotalMem(),
                self.findUptime(),
                self.findPlatform(),
                self.findSerialNumber(),
                self.findHost(),
                self.findHostname(),
                self.findName(),
                self.findSystemMac()
                )

            details = {}

            for item in items:
                details.update(item)

            # details = {'hostname': hostname, 'connect_ip': connect_ip, 'platform': platform,
            #               'version': sh_ver, 'serial_number': serial_number, 'system_uptime': uptime,
            #               'cpu_utilization': cpu_utilization, 'free_system_memory': free_memory,
            #               'total_sytem_memory': total_memory, 'vendor': 'arista'}

            return details

    # ----------------------------------------------------------------

                        
    class eapiRouting(object):
        """docstring for eapiRouting"""
        def __init__(self):
            super(eapiRouting, self).__init__()

        # ----------------------------------------------------------------
        # FIND ROUTING INFORMATION
        # ----------------------------------------------------------------

        def findRoutes(self, options=None):
            if options:
                routes = eapi._runCMDText(self, ['show ip route {0}\
                    '.format(options)])[0]['output']
            else:
                routes = eapi._runCMDText(self, ['show ip route'])[0]['output']
            
            return standardRoutes.findRoutes(routes)

        def findARP(self, options=None):
            if options:
                return eapi._runCMD(self, ['show arp {0}\
                    '.format(options)])[0]
            else:
                return eapi._runCMD(self, ['show arp'])[0]

        # ----------------------------------------------------------------
                        

    class eapi(eapiRouting, eapiInfo):
        """docstring for arista"""
        def __init__(self):
            super(eapi, self).__init__()
            self._host = None
            self._username = None
            self._password = None
            self._switch = None
            self._name = None
            self._version_info = None
            self._connected = False

        def __str__(self):
            return str(self.findDetails())

        # ----------------------------------------------------------------
        # "Private / Protected" Methods
        # ----------------------------------------------------------------

        def __connectToSwitch(self):
            try:
                return Server('https://{0}:{1}@{2}/command-api\
                    '.format(self._username, self._password, self._host))
            except Exception as e:
                print ('There was an error trying to connect: {}'.format(e))

        # run CMD
        def _runCMD(self, cli):
            if self._connected:
                return self._switch.runCmds(1, cli)
            else:
                self.connect()
                return self._switch.runCmds(1, cli)

        # run non JSON CMD
        def _runCMDText(self, cli):
            if self._connected:
                return self._switch.runCmds(1, cli, 'text')
            else:
                self.connect()
                return self._switch.runCmds(1, cli, 'text')

        @classmethod
        def createDataDict(cls, key, value):
            return {key: value}

        # ----------------------------------------------------------------
        # Public / Unprotected Methods
        # ----------------------------------------------------------------

        # creates connection to switch
        def connect(self):
            try:
                self._switch = self.__connectToSwitch()
                self._connected = True
                return self._switch
            except Exception as e:
                print ('Could not connect, error: {0}'.format(e))

        def setLogin(self, username, password):
            self._username = username
            self._password = password

        def initialize(self, host, name):
            self._host = host
            self._name = name

else:
    print('Python {0} is not supported at this time.'.format(sys.version_info[0:3]))
    print("Only version greater than 2.7.2 and less then 3.0 are supported")
    sys.exit(1)
