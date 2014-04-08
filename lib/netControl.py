#!/usr/bin/env python


from pnil.utils.utils import initArgs
from pnil.lib.eapi import eapi

class netDevice(object):
    """
        Parent class switch, which other classes will inherit from,
        ie. arista, cisco, juniper and so on
    """
    def __init__(self, args=None):
        '''
        Pass a dictionary of values such as:
            {
                'ip': [ip_address] or 'dns_name': 'hostname', (at least one mandatory)
                'manufacturer': 'arista' or 'cisco'..,  (mandatory)
                'function' or 'cli': [function_to_call], (optional, can be called later with dev.run('function'))
                'user': 'username', (optional - default set)
                'pass': 'password', (optional - default set)
            }
        '''
        super(netDevice, self).__init__()
        # defaults for now, building methods
        self._args = args if args else initArgs()
        self._net_device = None
        self._createNetDevice()

    def __dir__(self):
        funcs = dir(self._net_device)
        new_dir = []
        for each in funcs:
            if not (each.startswith('__') or each.startswith('_')):
                new_dir.append(each)

        return new_dir

    # ----------------------------------------------------------------
    # "Private / Protected" Methods
    # ----------------------------------------------------------------

    # creates the device self._net_device
    def _createNetDevice(self):
        if not self._args:
            self._args = initArgs()

        if self._args['manufacturer']:
            if self._args['manufacturer'].lower() == 'arista' or \
                self._args['manufacturer'].lower() == 'eapi':

                self._net_device = eapi()
            else:
                pass
        else:
            raise Exception('Please enter the manufacturer information')

    # set devices important variables
    def _initDevice(self):
        user = self._args['user']
        password = self._args['pass']


        host = self._args['dns_name'] if self._args['dns_name'] else self._args['ip_address']

        if user and password:
            self._net_device.setLogin(self._args['user'], self._args['pass'])

        if host:
            self._net_device.setHost(host)
        else:
            raise Exception('You must enter at least a dns_name or ip_address')

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

    def _getFunction(self, func=None):
        if not func:
            for key in self._args.keys():
                if key == 'cli' and self._args['cli']:
                    return  self._args['cli']
                elif key == 'function' and self._args['function']:
                    return self._args['function']
        else:
            return func

    # ----------------------------------------------------------------
    # Public / Unprotected Methods
    # ----------------------------------------------------------------

    # decides which method to run based on self._api_call
    # methods can also be called directly, but this simplifies it to the "caller"
    # by only needing to know one function or the cli command to to call.
    def run(self, func=None):
        '''
        Checks implemented_methods constant and tests if library has called method.
        otherwise terminates with mothod not implemented.
        '''

        # initilizes the network device and gets ready to run command.
        self._initDevice()

        implemented_methods = dir(self._net_device)

        function = self._getFunction(func)

        if not function:
            self._displayError()
        elif function not in implemented_methods:
            self._displayError()
        else:
            # getattr uses a string and passes as function call
            return getattr(self._net_device, function)()

    def getCmdEntered(self):
        return self._getFunction()
