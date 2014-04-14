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
    name = args['name'] if args['name'] else 'netDevice'

    # create device with ip_address or dns_name and manufacturer info
    _host = args['ip_address'] if args['ip_address'] else args['dns_name']

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
ARGUMENTS = False
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
        function = args['function'] if args['function'] else None

        sw1 = build(args)
        result = sw1.run(function, args)

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
        cisco_str = '''Codes: C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route

        Gateway of last resort is 10.16.0.1 to network 0.0.0.0

        C    192.168.31.0/24 is directly connected, Vlan31
             66.0.0.0/24 is subnetted, 1 subnets
        B       66.176.87.0 [200/0] via 10.16.0.1, 1d16h
             10.0.0.0/8 is variably subnetted, 6 subnets, 3 masks
        C       10.17.31.0/24 is directly connected, Vlan31
        C       10.16.0.2/32 is directly connected, Loopback0
        C       10.16.1.0/30 is directly connected, GigabitEthernet1/48
        O       10.16.0.1/32 [110/2] via 10.16.1.1, 1w0d, GigabitEthernet1/48
        C       10.17.33.0/24 is directly connected, Vlan33
        C       10.17.37.0/24 is directly connected, Vlan37
        C    192.168.33.0/24 is directly connected, Vlan33
        B*   0.0.0.0/0 [200/0] via 10.16.0.1, 1w0d'''

        result = standardRoutes.getRoutes(cisco_str)

        printResult(result, manufacturer='cisco')


if __name__ == '__main__':
    main()
