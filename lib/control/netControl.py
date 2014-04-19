#!/usr/bin/env python


from __future__ import print_function
from pnil.lib.arista.eapi import eapi
from pnil.lib.cisco.onepk import onepk
from pnil.utils.tools import initArgs
from itertools import izip_longest
import sys, string, random
import re

class netDevice(object):
    """
        Parent class switch, which other classes will inherit from,
        ie. arista, cisco, juniper and so on
    """
    def __init__(self, USE_ARGS=None):
        super(netDevice, self).__init__()
        self._net_device = None
        self._created = False
        self._name = None
        self._host = None
        self._method = None
        self._manufacturer = None
        self._initialized = False
        self._method_options = {'vrf': None, 'options': None}
    
        if USE_ARGS == True:
            args = initArgs()
            self.parseArguments(args)

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
            if manufacturer.lower() in ['arista', 'eapi']:

                self._net_device = eapi()
                self._created = True
            elif manufacturer.lower() in ['cisco', 'onepk']:

                self._net_device = onepk()
                self._created = True
            else:
                pass
        else:
            raise Exception('Please enter the manufacturer information')

    def _id_generator(self):
        digits = ''.join(random.choice('012345689') for _ in range(4))
        self._name = 'NET' + digits
        return self._name

    # ----------------------------------------------------------------
    # Public / Unprotected Methods
    # ----------------------------------------------------------------

    def parseArguments(self, args):
        # sets dev_name if -n is used
        if args['name']:
            self._name = args['name']
        # if -n is not used, then a random generated ID will be assigned
        else:
            # print('Device name not entered, picking random name')
            self._id_generator()

        # set the host from the list of args
        if args['ip_address']:
            self._host = args['ip_address'] 
        elif args['hostname']:
            self._host = args['hostname']
        else:
            print('Must specify the device to connected, please enter\
                hostname or IP address.')
            sys.exit(1)

        # set the manufacturer to make calls on
        if args['manufacturer']:
            self._manufacturer = args['manufacturer'] 
            self._createNetDevice(self._manufacturer)
        else:
            print('Remember to enter the manufacturer by passing the -m flag.')
            print('Also see -h for help on supported arguments')
            sys.exit(1)

        # initializes the device on information passed
        self.initialize(self._host)

        username = args['username'] if args['username'] else None
        password = args['password'] if args['password'] else None

        if username and password:
            self._net_device.setLogin(username, password)
        elif username:
            password = raw_input('Please enter password for {0}'.format(username))
            self._net_device.setLogin(username, password)
        else:
            username = raw_input('Enter the username: ')
            password = raw_input('Enter the password: ')
            self._net_device.setLogin(username, password)

        # sets the method(s) to be called if passed into the arguments
        if args['function'] and args['vrf'] or args['options']:
            self._method = self._findMethod(args['function'])
            self._method_options['vrf'] = args['vrf'] if args['vrf'] else None
            self._method_options['options'] = args['options'] if args['options'] else None
        elif args['function']:
            self._method = self._findMethod(args['function'])

        return self._net_device


    # decides which method to run based on self._api_call
    # methods can also be called directly, but this simplifies it to the "caller"
    # by only needing to know one method or the cli command to to call.
    def initialize(self, host, manufacturer=None, name=None):

        if name:
            self._name = name
        elif not self._name and not name:
            self._name = self._id_generator()

        if self._created:
            self._net_device.initialize(host, self._name)
        elif not self._created and manufacturer:
            self.create(manufacturer)
            self._net_device.initialize(host, self._name)
        else:
            raise Exception('Must create device first, call create(manufacturer)')

        self._initialized = True

    def setLogin(self, username=None, password=None):

        if username and password:
            self._net_device.setLogin(username, password)
        elif username:
            password = raw_input('Please enter password for {0}'.format(username))
            self._net_device.setLogin(username, password)
        else:
            username = raw_input('Enter the username: ')
            password = raw_input('Enter the password: ')
            self._net_device.setLogin(username, password)

    def create(self, manufacturer):
        if not self._created:
            return self._createNetDevice(manufacturer)
        else:
            return self._net_device

    @classmethod
    def _findMethod(cls, func):
        
        func_calls = re.split(r'\W+', func)
        new_calls = []

        if len(func_calls) > 1:
            for call in func_calls:
                new_calls.append(call.lstrip().rstrip())
        else:
            new_calls.append(func_calls[0].lstrip().rstrip())

        return new_calls

    @classmethod
    def _findCMDOptions(cls, func_options):
        if func_options['vrf'] and func_options['options']:
            new_opts = ' '.join(['vrf', func_options['vrf'], func_options['options']])
        elif func_options['vrf']:
            new_opts = ' '.join(['vrf', func_options['vrf']])
        elif func_options['options']:
            new_opts = ' '.join([func_options['options']])

        return new_opts

    def runEAPI(self, method=None, method_options=None):
        implemented_methods = dir(self._net_device)

        if method_options:
            self._method_options = method_options

        if not self._method and type(method) is not dict:
            self._method = self._findMethod(method)
        elif not self._method and type(method) is dict:
            self._method = self._findMethod(method['method'])

        result = [] if len(self._method) > 1 else {}

        counter = 1
        if len(self._method) > 1:
            for call in self._method:
                if call not in implemented_methods:
                    result.append({counter: {'method_not_found': [call]}})
                    counter += 1
                else:
                    result.append({counter: getattr(self._net_device, call)()})
                    counter += 1

        elif self._method[0] not in implemented_methods:
            result.update({'method_not_found': self._method[0]})
        elif self._method_options['vrf'] or self._method_options['options']:
            new_opts = self._findCMDOptions(self._method_options)
            result = getattr(self._net_device, self._method[0])(new_opts)
        else:
            result = getattr(self._net_device, self._method[0])()

        return result

    def runONEPK(self, method=None):
        implemented_methods = dir(self._net_device)

        result = [] if len(self._method) > 1 else {}

        counter = 1
        if len(self._method) > 1:
            for call in self._method:
                if call not in implemented_methods:
                    result.append({counter: {'method_not_found': [call]}})
                    counter += 1
                else:
                    result.append({counter: getattr(self._net_device, call)()})
                    counter += 1
        else:
            result = getattr(self._net_device, self._method[0])()

        return result


    def run(self, method=None, method_options=None):
        '''
        Checks implemented_methods constant and tests if library has called method.
        otherwise terminates with mothod not implemented.
        '''
        # initializes the device with proper information passed
        if not self._initialized:
            raise Exception("initialize device first, see help(netDevice) for more info")

        if self._manufacturer.lower() == 'arista' or \
            self._manufacturer.lower() == 'eapi':

            return self.runEAPI(method, method_options)

        if self._manufacturer.lower() == 'cisco' or \
            self._manufacturer.lower() == 'onepk':

            return self.runONEPK(method)

    def getManufacturer(self):
        return self._manufacturer
