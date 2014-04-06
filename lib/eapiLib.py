#!/usr/bin/env python

#----------------------------------------------------------------

''' Library to make Arista Networks eAPI calls, furthur documenttion later '''

#----------------------------------------------------------------

#----------------------------------------------------------------
# Import Server JSON RPC library
#----------------------------------------------------------------

from jsonrpclib import Server
import argparse

#----------------------------------------------------------------

#----------------------------------------------------------------
# Configuration section
#----------------------------------------------------------------
# _ip = "IP address of Arista Switch"
# _cli ==> Enter the CLI command to run
# _user = '_user with api/admin access'
# _pass = '_pass'
#----------------------------------------------------------------

IMPLEMENTED_METHODS = {'intfStatus': 'show interfaces status'}

# function to check for correct IP Address Input
# this function can later be part of  a larger check_input.py or similar
def checkIP(ipAddress):
    ''' Checks a given ipAddress for validity (first octect only for now)'''
    lip = ipAddress.split('.')
    if int(lip[0]) <= 0 or int(lip[0]) > 223:
        raise ValueError('Invalid IP')
    
    return ipAddress      


class Switch(object):
    """
        Parent class switch, which other classes will inherit from, 
        ie. arista, cisco, juniper and so on
    """
    def __init__(self):
        # defaults for now, building methods
        self._cli = ''
        self._ip = ''
        self._user, self._pass = 'admin', 'arista'
        self._cliCall = ''
        self._response = []

    # initialize command line arguments 
    def _initArgs(self):
        parser = argparse.ArgumentParser(description='\
            input -f [function] -i [ipAddress] \
            -u [username] -p [password]'\
            )

        parser.add_argument('-f', '--function', help='i.e. -f IntfStatus, show version')
        parser.add_argument('-c', '--cli', help='i.e. same as -f, for redundancy')
        parser.add_argument('-i', '--ip_address', help='i.e. -i "192.168.31.21"')
        parser.add_argument('-u', '--username', help='Enter username of device')
        parser.add_argument('-p', '--password', help='Enter password for username')
        arg = parser.parse_args()

        # load function to call
        if arg.function:
            self._cli = arg.function
        elif arg.cli:
            self._cli = arg.cli
        else:
            raise ValueError('Please choose what to do, i.e: -f intfStatus')

        # set ip address to make calls on
        if arg.ip_address:
            self._ip = checkIP(arg.ip_address)
        else:
            raise ValueError('Please enter the IP address. ie: -i "192.168.31.21"')

        # set username and password if entered, otherwise default
        if arg.username:
            self._user = arg.username
        if arg.password:
            self._pass = arg.password

    def showVer(self):
        pass

    def showRoute(self, ipVersion):
        pass

    def intfStatus(self):
        pass
            

class arista(Switch):
    """docstring for arista"""
    def __init__(self):
        super(arista, self).__init__()
        self._intfStatus = {}
        
        self._initArgs()


    # function returns a dictionary of the interfaces and their status
    def intfStatus(self):
        switch = Server('https://%s:%s@%s/command-api' %
                  (self._user, self._pass, self._ip))
        self._response = switch.runCmds(1, [IMPLEMENTED_METHODS[self._cliCall]])

        self._intfStatus = self._response[0]['interfaceStatuses']
        return self._intfStatus


    # decides which method to run based on self._cli
    # methods can also be called directly, but this simplifies it to the "caller"
    # by only needing to know one function or the cli command to to call.
    def runCmd(self):
        ''' 
        Checks IMPLEMENTED_METHODS constant and tests if library has called method.
        otherwise terminates with mothod not implemented.
        '''

        if self._cli not in IMPLEMENTED_METHODS.keys() and \
        self._cli not in IMPLEMENTED_METHODS.values():
            print 'only methods available now are:'
            for k, v in IMPLEMENTED_METHODS.items():
                print "\t%s: %s" % (k, v)
            raise ValueError('Method not yet implemented')

        elif self._cli in IMPLEMENTED_METHODS.keys():
            self._cliCall = self._cli
            return  getattr(self, self._cliCall)() #getattr uses a string and passes as function call
        else:
            # finds a key from a given dictionary value
            rKey = [key for key, value in IMPLEMENTED_METHODS.iteritems() \
                        if value == IMPLEMENTED_METHODS[key]]
            self._cliCall = rKey[0]
            return getattr(self, self._cliCall)()
