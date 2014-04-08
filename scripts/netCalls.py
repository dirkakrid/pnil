#!/usr/bin/env python

'''Module to test calls to eapLib'''

#----------------------------------------------------------------

from pnil.lib.netControl import netDevice
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
    if rtr_type is dict or rtr_type is list:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(l_status)
    else:
        print (l_status)


#----------------------------------------------------------------


def main():
    '''Ran only if program called by itself'''
    
    # args = {'host': 'veos-02', 'manufacturer': 'arista',
    #     'cli': 'showIntfStatus', 'ip_address': '', 'user': 'arista', 'pass': 'arista'}
    # switch = netDevice(args=args)

    switch = netDevice()
    result = switch.run()

    if result:
        # printResult(showDisabledIntf(result))
        # print ('\n')
        # printResult(showConnectedIntf(result))
        printResult(result)


if __name__ == '__main__':
    main()
