#!/usr/bin/env python


from pnil.lib.eapi import eapi
from pnil.lib.onepk import onepk
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

    def __str__(self):
        r_str = self._net_device.__str__()
        return r_str

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
            elif manufacturer.lower() == 'cisco' or \
                manufacturer.lower() == 'onepk':

                self._net_device = onepk()
                self._created = True
            else:
                pass
        else:
            raise Exception('Please enter the manufacturer information')

    # ----------------------------------------------------------------
    # Public / Unprotected Methods
    # ----------------------------------------------------------------

    # decides which method to run based on self._api_call
    # methods can also be called directly, but this simplifies it to the "caller"
    # by only needing to know one function or the cli command to to call.

    def initialize(self, host, manufacturer, name='net1'):
        if self._created:
            self._net_device.initialize(host, name)
        elif not self._created and manufacturer:
            self.create(manufacturer)
            self._net_device.initialize(host, name)
        else:
            raise Exception('Must create device first, call create(manufacturer)')

        self._initialized = True

    def setLogin(self, user, password):
        self._net_device.setLogin(user, password)

    def create(self, manufacturer):
        if not self._created:
            return self._createNetDevice(manufacturer)
        else:
            return self._net_device

    def displayError(self):
        print ('****************************************************************')
        print ('\n')
        print ('IP Address (-i), manufacturer (-m), AND one of')
        print ('the following functions (-f) are required')
        print ('Use \'python main.py -h\' for more info on proper usage')
        print ('The function called is not in the methods implemented')
        print ('\n')
        print ('*************************SEE BELOW****************************')
        funcs = dir(self._net_device)
        for each in funcs:
            if not (each.startswith('__') or each.startswith('_')):
                print ('*** ' + each)

    @classmethod
    def _getFunction(cls, func):
        
        func_calls = func.split(',')
        new_calls = []
        if len(func_calls) > 1:
            for call in func_calls:
                new_calls.append(call.lstrip().rstrip())
        else:
            new_calls.append(func_calls[0].lstrip().rstrip())

        return new_calls

    def run(self, function, args=None):
        '''
        Checks implemented_methods constant and tests if library has called method.
        otherwise terminates with mothod not implemented.
        '''
        # initializes the device with proper information passed
        if not self._initialized:
            raise Exception("initialize device first, see help(netDevice) for more info")

        implemented_methods = dir(self._net_device)
        func_call = self._getFunction(function)

        result = [] if len(func_call) > 1 else None

        if len(func_call) > 1:
            for call in func_call:
                if call not in implemented_methods:
                    self.displayError()
                    continue
                result.append(getattr(self._net_device, call)())
        else:
            if func_call[0] not in implemented_methods:
                self.displayError()
            elif args is not None:
                if args['vrf'] or args['options']:
                    result = getattr(self._net_device, func_call[0])(args)
                else:
                    result = getattr(self._net_device, func_call[0])()
            else:
                result = getattr(self._net_device, func_call[0])()

        return result
