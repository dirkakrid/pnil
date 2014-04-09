#!/usr/bin/env python


from pnil.lib.eapi import eapi
from itertools import izip_longest

class netDevice(object):
    """
        Parent class switch, which other classes will inherit from,
        ie. arista, cisco, juniper and so on
    """
    def __init__(self):
        super(netDevice, self).__init__()
        # defaults for now, building methods
        self._net_device = None
        self._initialized = False
        self._created = False
        self._function = None

    def __dir__(self):
        net_list = sorted(dir(self._net_device))
        self_list = sorted(set((dir(type(self))+list(self.__dict__))))
        new_dir = [
            {
            'local_methods':[],
            'remote_methods':[]
            }
        ]

        for s_list, n_list in izip_longest(self_list, net_list):
            if s_list:
                if not (s_list.startswith('__') or s_list.startswith('_')):
                    new_dir[0]['local_methods'].append(s_list)

            if n_list:
                if not (n_list.startswith('__') or n_list.startswith('_')):
                    new_dir[0]['remote_methods'].append(n_list)

        return new_dir

    # ----------------------------------------------------------------
    # "Private / Protected" Methods
    # ----------------------------------------------------------------

    # creates the device self._net_device
    def _createNetDevice(self, manufacturer):

        if manufacturer:
            if manufacturer.lower() == 'arista' or \
                manufacturer.lower() == 'eapi':

                self._net_device = eapi()
                self._created = True
            else:
                pass
        else:
            raise Exception('Please enter the manufacturer information')

    def _displayError(self):
        print '********************************************************'
        print '***IP Address (-i), manufacturer (-m), AND one of*******'
        print '***the following functions (-f) are required************'
        print "***Use 'python main.py -h' for more info on proper usage"
        print '********************************************************'
        funcs = dir(self._net_device)
        for each in funcs:
            if not (each.startswith('__') or each.startswith('_')):
                print '*** ' + each

    def _getFunction(self, func):
        try:
            self._function = func
            return self._function
        except Exception, e:
            raise e

    # ----------------------------------------------------------------
    # Public / Unprotected Methods
    # ----------------------------------------------------------------

    # decides which method to run based on self._api_call
    # methods can also be called directly, but this simplifies it to the "caller"
    # by only needing to know one function or the cli command to to call.

    def initialize(self, host, manufacturer, user=None, password=None):
        if not self._created:
            self._createNetDevice(manufacturer)

        if host and user and password:
            self._net_device.setAll(host, user, password)
        elif host:
            self._net_device.setHost(host)
        else:
            raise Exception('Enter at least the host to connect to')

        self._initialized = True

    def setLogin(self, user, password):
        self._net_device.setLogin(user, password)

    def setHost(self, host, manufacturer=None):
        if self._created:
            self._net_device.setHost(host)
        elif not self._created and manufacturer:
            self.create(manufacturer)
            self.setHost(host)
        else:
            raise Exception('Must create device first, call create(manufacturer)')

        self._initialized = True

    def create(self, manufacturer):
        if not self._created:
            return self._createNetDevice(manufacturer)
        else:
            return self._net_device

    def run(self, func=None):
        '''
        Checks implemented_methods constant and tests if library has called method.
        otherwise terminates with mothod not implemented.
        '''
        # initializes the device with proper information passed
        if not self._initialized:
            raise Exception("initialize device first, see help(netDevice) for more info")

        implemented_methods = dir(self._net_device)

        if not func:
            self._displayError()
        elif func not in implemented_methods:
            self._displayError()
        else:
            func_call = self._getFunction(func)
            return getattr(self._net_device, func_call)()

    def getCmdEntered(self):
        return self._function
