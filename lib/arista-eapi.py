#!/usr/bin/env python

# ----------------------------------------------------------------

''' Library to make Arista Networks eAPI calls, furthur documenttion later '''

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Import Server JSON RPC library
# ----------------------------------------------------------------

from jsonrpclib import Server
import pprint

# ----------------------------------------------------------------

# ----------------------------------------------------------------
# Configuration section
# ----------------------------------------------------------------
# _ip = "IP address of Arista Switch"
# _cli ==> Enter the CLI command to run
# _user = '_user with api/admin access'
# _pass = '_pass'
# ----------------------------------------------------------------

class arista-eapi(object):
    """docstring for arista"""
    def __init__(self):
        super(arista, self).__init__()
        self._cli = ''
        self._ip = ''
        self._user, self._pass = 'admin', 'arista'
        self._response = {}
        self.connection = self.connect()

    def connect(self):
        switch = Server('https://%s:%s@%s/command-api' %
                        (self._user, self._pass, self._ip))
        return switch

    # run CMD
    def runCMD(self, cli):
        return self.connection.runCmds(1, [cli])

    # function returns a dictionary of the interfaces and their status
    def showIntfStatus(self):
        self._response = self.runCMD('show interfaces status')

        return self._response[0]['interfaceStatuses']
