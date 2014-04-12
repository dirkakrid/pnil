#!/usr/bin/env python

'''Module to test calls to eapLib'''

#----------------------------------------------------------------

from pnil.lib.netControl import netDevice
from pnil.utils import tools
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

def printConnected(result):
    print ('# ' + '-'*110)
    print ('# CONNECTED ROUTES')
    print ('# ' + '-'*110)
    for prefix, values in result['C'].iteritems():
        print ('# Prefix: {0}\tAD/Metric: {1}\tNext-Hop:{2}\tNext-Hop-Interface: {3}\
                    '.format(prefix, values['ad_metric'], values['next_hop'], values['next_hop_int']))

    print ('# ' + '-'*110)

def printStatics(result):
    print ('# ' + '-'*110)
    print ('# STATIC ROUTES')
    print ('# ' + '-'*110)
    for prefix, values in result['S'].iteritems():
        print ('# Prefix: {0}\tAD/Metric: {1}\tNext-Hop:{2}\tNext-Hop-Interface: {3}\
                    '.format(prefix, values['ad_metric'], values['next_hop'], values['next_hop_int']))

    print ('# ' + '-'*110)

def printOSPF(result):
    ospf_keys = ['O', 'O IA', 'O E2', 'O E1', 'O N1', 'O N2']
    print ('# ' + '-'*110)
    print ('# OSPF ROUTES')
    print ('# ' + '-'*110)
    for key in ospf_keys:
        if key in result.keys():
            for prefix, values in result[key].iteritems():
                print ('# Prefix: {0}\tAD/Metric: {1}\tNext-Hop:{2}\tNext-Hop-Interface: {3}\
                    '.format(prefix, values['ad_metric'], values['next_hop'], values['next_hop_int']))

    print ('# ' + '-'*110)

def findByProtocol(result, protocol='S'):
    if protocol.lower() == 'c' or protocol.lower() == 'connected':
        printConnected(result)
    elif protocol.lower() == 's' or protocol.lower() == 'static':
        printStatics(result)
    elif protocol.lower() == 'o' or protocol.lower() == 'ospf':
        printOSPF(result)

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

    args = tools.initArgs()

    # ----------------------------------------------------------------
    # For running with with command-line arguments
    # ----------------------------------------------------------------
    dev = build(args)
    result = run(dev, args)

    pp = pprint.PrettyPrinter(indent=2, width=60)
    if type(result) is not str and type(result) is not unicode:
        pp.pprint(result)
    else:
        print (result)
    #
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


if __name__ == '__main__':
    main()
