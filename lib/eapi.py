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
        self._api_call = None
        self._host = None
        self._user, self._pass = 'admin', 'arista'
        self._response = {}
        self._switch = None

    def _connectToSwitch(self):
        if self._host:
            switch = Server('https://{0}:{1}@{2}/command-api'.format(self._user, self._pass, self._host))
            return switch
        else:
            raise ValueError('IP address not set or invalid')

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

    # run CMD
    def _runCMD(self, cli):
        if self._switch:
            return self._switch.runCmds(1, [cli])
        else:
            self.connect()
            return self._switch.runCmds(1, [cli])

    # function returns a dictionary of the interfaces and their status
    def showIntfStatus(self):
        self._response = self._runCMD('show interfaces status')

        return self._response[0]['interfaceStatuses']
