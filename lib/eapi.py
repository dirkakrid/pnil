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
# _ip = "IP address of Arista Switch"
# _cli ==> Enter the CLI command to run
# _user = '_user with api/admin access'
# _pass = '_pass'
# ----------------------------------------------------------------

class eapi(object):
    """docstring for arista"""
    def __init__(self):
        super(eapi, self).__init__()
        self._cli = None
        self._ip = None
        self._user, self._pass = 'admin', 'arista'
        self._response = {}
        self._switch = None

    def _connectToSwitch(self):
        if self._ip:
            switch = Server('https://%s:%s@%s/command-api' %
                        (self._user, self._pass, self._ip))
            return switch
        else:
            raise ValueError('IP address not set or invalid')

    # 
    def connect(self):
        self._switch = self._connectToSwitch()
        return self._switch

    # run CMD
    def runCMD(self, cli):
        if self._switch:
            return self._switch.runCmds(1, [cli])
        else:
            self.connect()
            return self._switch.runCmds(1, [cli])

    # function returns a dictionary of the interfaces and their status
    def showIntfStatus(self):
        self._response = self.runCMD('show interfaces status')

        return self._response[0]['interfaceStatuses']
