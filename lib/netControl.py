#!/usr/bin/env python


from pnil.utils.utils import initArgs
from pnil.lib.eapi import eapi

class netDevice(object):
    """
        Parent class switch, which other classes will inherit from,
        ie. arista, cisco, juniper and so on
    """
    def __init__(self, args=None):
        super(netDevice, self).__init__()
        # defaults for now, building methods
        self._args = args if args else initArgs()
        self._manufacturer = self._args['manufacturer']
        self._host = self._args['ip_address'] if self._args['ip_address'] else self._args['host']
        self._api_call = self._args['cli'] if self._args['cli'] else self._args['function']
        self._user, self._pass = self._args['user'], self._args['pass']
        self._net_device = None
        self._createNetDevice()

    # creates the device self._net_device
    def _createNetDevice(self):
        if not self._args:
            self._args = initArgs()

        if self._manufacturer:
            if self._manufacturer.lower() == 'arista' or self._manufacturer.lower() == 'eapi':
                self._net_device = eapi()
            else:
                pass
        else:
            raise ValueError('Please enter the manufactuer information')

    # set devices important variables
    def _initDevice(self):
        if self._user and self._pass:
            self._net_device.setLogin(self._user, self._pass)

        if self._host:
            self._net_device.setHost(self._host)
        else:
            raise ValueError('You must enter at least a host or ip_addres')

    def displayError(self):
        print '********************************************************'
        print '***IP Address (-i), manufacturer (-m), AND one of*******'
        print '***the following functions (-f) are required************'
        print "***Use 'python main.py -h' for more info on proper usage"
        print '********************************************************'
        funcs = dir(self._net_device)
        for each in funcs:
            if not (each.startswith('__') or each.startswith('_')):
                print '*** ' + each

    # decides which method to run based on self._api_call
    # methods can also be called directly, but this simplifies it to the "caller"
    # by only needing to know one function or the cli command to to call.
    def run(self):
        '''
        Checks implemented_methods constant and tests if library has called method.
        otherwise terminates with mothod not implemented.
        '''

        # initilizes the network device and gets ready to run command.
        self._initDevice()

        implemented_methods = dir(self._net_device)
        #print implemented_methods

        if not self._api_call:
            self.displayError()
        elif self._api_call not in implemented_methods:
            self.displayError()
        else:
            # getattr uses a string and passes as function call
            return getattr(self._net_device, self._api_call)()
