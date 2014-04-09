#!/usr/bin/env python

'''Module to test calls to eapLib'''

#----------------------------------------------------------------

from pnil.lib.netControl import netDevice
import argparse
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


def printResult(l_status):
    rtr_type = type(l_status)
    if rtr_type is list:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(l_status)
    elif rtr_type is dict:
        for key, value in l_status.items():
            if len(key) > 13:
                print ('{0}: \t{1}'.format(key, value))
            else:
                print ('{0}: \t\t{1}'.format(key, value))
    else:
        print (l_status)


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

def run(dev, function):
    if function:
        value = dev.run(function)
    else:
        value = dev.displayError()

    return value

def main():
    '''
    Ran only if program called as script
    '''

    parser = argparse.ArgumentParser(description='\
        input -f [function] -i [ipAddress] \
        -u [username] -p [password]')

    parser.add_argument('-f', '--function', help='i.e. -f getHostname, getVersion...')
    parser.add_argument('-c', '--cli', help='i.e. same as -f, for redundancy')
    parser.add_argument('-i', '--ip_address', help='i.e. -i "192.168.31.21"')
    parser.add_argument('-d', '--dns_name', help='i.e. -h sw01.domain.com')
    parser.add_argument('-u', '--username', help='Enter username of device')
    parser.add_argument('-p', '--password', help='Enter password for username')
    parser.add_argument('-n', '--name', help='Enter the device\'s name. i.e -n sw1')
    parser.add_argument('-m', '--manufacturer', help='Enter the manufacturer to run on\
        i.e => -m arista')
    _args = vars(parser.parse_args())

    # _args = {
    #     'function': 'getHostname',
    #     'dns_name': 'eos-sw01',
    #     'manufacturer': 'arista',
    #     'name': 'sw1',
    #     'cli': None,
    #     'ip_address': None,
    #     'username': None,
    #     'password': None
    # }

    dev = build(_args)

    # sets the function based on the command-line argument passed -f or -c
    function = _args['function'] if _args['function'] else _args['cli']

    result = run(dev, function)

    if result:
        printResult(result)

    # Interpreter simulation
    # sw1 = netDevice()
    # sw1.initialize('eos-sw01', 'arista')
    # list_dir = dir(sw1)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(list_dir)

    # prettyfying the printing of dir() call, just testing
    # for i in list_dir:
    #     for key, value in i.items():
    #         for j in range(0, len(value)):
    #             print "{0}:\t{1}".format(key, value[j])


if __name__ == '__main__':
    main()
