#!/usr/bin/env python

'''Module to test calls to eapLib'''

#----------------------------------------------------------------

from pnil.lib.netControl import netDevice
from pnil.utils.tools import utils, routingInfo, printRouting
import pprint

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

def getFunction(args):
    return args['function'] if args['function'] else args['cli']

def run(dev, args):
    function = args['function'] if args['function'] else args['cli']
    vrf = args['vrf'] if args['vrf'] else None
    if function:
        if vrf:
            value = dev.run(function, vrf)
        else:
            value = dev.run(function)
    else:
        value = dev.displayError()

    return value

def runInterpreter(dev, args):
    function = args[0]
    vrf = args[1]
    if function:
        if vrf:
            value = dev.run(function, vrf)
        else:
            value = dev.run(function)
    else:
        value = dev.displayError()

    return value

def main():
    '''
    Ran only if program called as script
    '''

    args = utils.initArgs()

    # ----------------------------------------------------------------
    # For running with with command-line arguments
    # ----------------------------------------------------------------
    dev = build(args)
    result = run(dev, args)

    # pp = pprint.PrettyPrinter(indent=2, width=60)
    # if type(result) is not str and type(result) is not unicode:
    #     pp.pprint(result)
    # else:
    #     print (result)

    print ('# ' + '-'*110)
    print ('# PRINTING ARISTA ROUTES')
    print ('# ' + '-'*110)
    printRouting.findByProtocol(result, 'Connected')
    printRouting.findByProtocol(result, 'Static')
    printRouting.findByProtocol(result, 'OSPF')

    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # testing output as if running from interpreter, by passing arguments directly
    # and manually initializing the device
    # ----------------------------------------------------------------
    # sw1 = netDevice()
    # sw1.initialize('veos-m-01', 'arista', 'sw1')
    # # function = 'getHostname, getVersion, getPlatform, getCPU, getDetails'
    # function = 'getRoutesDetail'
    # result = runInterpreter(sw1, [function, 'default'])
    # pp = pprint.PrettyPrinter(indent=2, width=60)
    # if type(result) is not str and type(result) is not unicode:
    #     pp.pprint(result)
    # else:
    #     print (result)
    # findByProtocol(result, 'Connected')
    # findByProtocol(result, 'Static')
    # findByProtocol(result, 'OSPF')

    # ----------------------------------------------------------------
    # Testing Paramiko with a Cisco device
    # ----------------------------------------------------------------
    # import paramiko
    # rtr01 = paramiko.SSHClient()
    # rtr01.load_system_host_keys()
    # rtr01.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # rtr01.connect('rtr01', username='cisco', password='cisco')
    # stdin, stdout, stderr = rtr01.exec_command('show ip route')
    # print(stdout.readlines())

    # Till I figure out the paramiko exception, raw data input
    cisco_str = '''Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area 
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       + - replicated route, % - next hop override

        Gateway of last resort is 66.176.87.1 to network 0.0.0.0

        S*    0.0.0.0/0 [1/0] via 66.176.87.1, GigabitEthernet0/0
              10.0.0.0/8 is variably subnetted, 7 subnets, 3 masks
        C        10.16.0.1/32 is directly connected, Loopback0
        O        10.16.0.2/32 [110/2] via 10.16.1.2, 5d14h, GigabitEthernet0/1
        C        10.16.1.0/30 is directly connected, GigabitEthernet0/1
        L        10.16.1.1/32 is directly connected, GigabitEthernet0/1
        B        10.17.31.0/24 [200/0] via 10.16.0.2, 5d14h
        B        10.17.33.0/24 [200/0] via 10.16.0.2, 5d14h
        B        10.17.37.0/24 [200/0] via 10.16.0.2, 4d11h
              66.0.0.0/8 is variably subnetted, 2 subnets, 2 masks
        C        66.176.87.0/24 is directly connected, GigabitEthernet0/0
        L        66.176.87.64/32 is directly connected, GigabitEthernet0/0
              76.0.0.0/32 is subnetted, 1 subnets
        S        76.96.92.197 [254/0] via 66.176.87.1, GigabitEthernet0/0
        B     192.168.31.0/24 [200/0] via 10.16.0.2, 5d14h
        B     192.168.33.0/24 [200/0] via 10.16.0.2, 5d14h'''
    cisco_list = cisco_str.split('\n')
    cisco_routes = routingInfo.getRoutesDetail(cisco_list)
    # if type(cisco_routes) is not str and type(cisco_routes) is not unicode:
    #     pp.pprint(cisco_routes)
    # else:
    #     print (cisco_routes)
    print ('# ' + '-'*110)
    print ('# PRINTING CISCO ROUTES')
    print ('# ' + '-'*110)
    printRouting.findByProtocol(cisco_routes, 'Connected')
    printRouting.findByProtocol(cisco_routes, 'Static')
    printRouting.findByProtocol(cisco_routes, 'OSPF')
    printRouting.findByProtocol(cisco_routes, 'BGP')


if __name__ == '__main__':
    main()
