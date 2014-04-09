#!/usr/bin/env python

'''Module to test calls to eapLib'''

#----------------------------------------------------------------

from pnil.lib.netControl import netDevice
from pnil.utils.utils import initArgs
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

def initDevice(args):
    pass

def main():
    '''Ran only if program called by itself'''

    switch = netDevice()
    # switch.initialize('eos-sw01', 'arista')

    switch.setHost('eos-sw01', 'arista')
    switch.setLogin('arista', 'arista')

    result = switch.run('getDetails')

    if result:
        printResult(result)

    # Interpreter simulation
    # sw1 = netDevice()
    # sw1.initialize('eos-sw01', 'arista')
    # list_dir = dir(sw1)
    # pp = pprint.PrettyPrinter(indent=4)
    # pp.pprint(list_dir)

    # for i in list_dir:
    #     for key, value in i.items():
    #         for j in range(0, len(value)):
    #             print "{0}:\t{1}".format(key, value[j])


if __name__ == '__main__':
    main()
