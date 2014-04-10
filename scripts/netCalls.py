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


def formatResult(result, func):
    '''
    Prints the result of the calling functions to screen with varying different types. 
    1) Checks if result is a list then calls the formatList() function.
    2) If the result is a dict, it calls  formatDict() function .
    3) if neigther, just simply prints out the result.
    '''

    function = func.split(',')

    if type(result) is list:
        return formatList(result, function)
    elif type(result) is dict:
        return formatDict(result)
    else:
        return formatSingle(result, function)

def formatSingle(result, func):
    new_result = {}
    new_result.update({func[0]: result})
    return new_result

def formatList(result, func):

    counter = 0
    new_result = {}
    for item in result:
        if type(item) is dict:
            for key, value in item.iteritems():
                # print ('{0}: \t{1}'.format(key, value))
                new_result.update({key: value})
        else:
            # print("{0}: \t{1}".format(func[counter].lstrip(), item))
            key = func[counter].lstrip().rstrip()
            new_result.update({key: item})
            counter += 1

    return new_result

def formatDict(result):
    new_result = result
    # for key, value in result.iteritems():
    #     new_result[key] = value

    return new_result

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

    # ----------------------------------------------------------------
    # For running with with command-line arguments
    # ----------------------------------------------------------------
    # dev = build(_args)
    # sets the function based on the command-line argument passed -f or -c
    # function = _args['function'] if _args['function'] else _args['cli']
    # result = run(dev, function)
    # pp = pprint.PrettyPrinter(indent=2)
    # pp.pprint(formatResult(result, function))
    # print (formatResult(result, function))
    #
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # Interpreter simulation of __dir__ overload
    # ----------------------------------------------------------------
    # sw1 = netDevice()
    # sw1.initialize('eos-sw01', 'arista')
    # list_dir = dir(sw1)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(list_dir)
    # prettyfying the printing of dir() call, just testing
    # for i in list_dir:
    #     for key, value in i.iteritems():
    #         for j in range(0, len(value)):
    #             print "{0}:\t{1}".format(key, value[j])
    #
    # ----------------------------------------------------------------

    # ----------------------------------------------------------------
    # testing output as if running from command-line
    # ----------------------------------------------------------------
    sw1 = netDevice()
    # sw2 = netDevice()
    sw1.initialize('eos-sw01', 'arista', 'sw1')
    # sw2.initialize('veos-01', 'arista', 'sw1')
    function = 'getIntfDetails, getDetails'
    # function = 'getDetails'
    result = run(sw1, function)
    # result2 = run(sw2, function)
    pp = pprint.PrettyPrinter(indent=2, width=40, depth=None)
    pp.pprint(formatResult(result, function))
    # print('\n\n')
    # pp.pprint(formatResult(result2, function))


if __name__ == '__main__':
    main()