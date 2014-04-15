#!/usr/bin/env python

'''Module to test calls to eapLib'''

#----------------------------------------------------------------

from pnil.lib.netControl import netDevice
from pnil.utils.tools import initArgs
from pnil.utils.findRoutes import standardRoutes
import pprint

#----------------------------------------------------------------

#----------------------------------------------------------------


def showDisabledIntf(_status):
    '''
      Sample code displays only the status if the interface is 'disabled'
    '''
    status_info = {}
    for int_key, int_status in _status.items():
        if int_status['linkStatus'] == 'disabled' or int_status['linkStatus'] == 'notconnect':
            status_info.update({int_key: [int_status['linkStatus'], int_status['description']]})

    return status_info


def showConnectedIntf(_status):
    '''
      Sample code displays only the status if the interface is 'disabled'
    '''
    status_info = {}
    for int_key, int_status in _status.items():
        if int_status['linkStatus'] == 'connected':
            status_info.update({int_key: [int_status['linkStatus'], int_status['description']]})

    return status_info

#----------------------------------------------------------------

# ----------------------------------------------------------------

def build(args):

    # sets dev_name if -n is used, otherwise generic 'dev' is used
    name = args['name'] if args['name'] else 'net1'

    # create device with ip_address or hostname and manufacturer info
    _host = args['ip_address'] if args['ip_address'] else args['hostname']

    net_dev = netDevice()
    net_dev.initialize(_host, args['manufacturer'], name)

    # if login information entered, use it, otherwise default
    if args['username'] and args['password']:
        net_dev.setLogin(args['username'], args['password'])

    return net_dev

# -------------------
# GLOBAL VARIABLES FOR PRINTING AND RUNNING
# -------------------
ARISTA = True
CISCO_IOS = False
ARGUMENTS = True
INTERPRETER_SIM = False if ARGUMENTS else True
# -------------------

def printResult(result, manufacturer='Arista'):
    pp = pprint.PrettyPrinter(indent=2, width=60)
    if type(result) is not str and type(result) is not unicode:
        print ('# ' + '-' * 80)
        print ('# {0} DATASTRUCTURE REPRESENTATION'.format(manufacturer.upper()))
        print ('# ' + '-' * 80 + '\n')
        pp.pprint(result)
        print ('\n# ' + '-' * 80 + '\n')
    else:
        print ('# ' + '-' * 80 + '\n')
        print (result)
        print ('\n# ' + '-' * 80 + '\n')

def main():
    '''
    Ran only if program called as script
    '''
    if ARISTA and ARGUMENTS:
        args = initArgs()

        sw1 = netDevice(args)
        result = sw1.run(args)

        printResult(result)


    if ARISTA and INTERPRETER_SIM:
        sw1 = netDevice()
        sw1.initialize('veos-01', 'arista', 'sw1')
        # # function = 'getHostname, getVersion, getPlatform, getCPU, getDetails'
        function = 'getRoutes'
        result = sw1.run(function)

        printResult(result)


    # Till I figure out the paramiko exception, raw data input
    if CISCO_IOS:
        pass


if __name__ == '__main__':
    main()
