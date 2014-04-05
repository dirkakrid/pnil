#!/usr/bin/env python

'''Module to test calls to eapLib'''

#----------------------------------------------------------------

from eapiLib import arista

#----------------------------------------------------------------

def returnIntfList(status_info):
    rtrList = []
    for key, value in status_info.items():
        rtrList.append(' {0}\t\t{1}    \t\t{2}'.format(key, value[0], value[1]))

    return rtrList


def getDisabledIntf(_status):
    '''
      Sample code displays only the status if the interface is 'disabled'
    '''
    status_info = {}
    for int_key, int_status in _status.items():
        if int_status['linkStatus'] == 'disabled':
            status_info.update({int_key: [int_status['linkStatus'], int_status['description']]})

    return returnIntfList(status_info)


def getConnectedIntf(_status):
    '''
      Sample code displays only the status if the interface is 'disabled'
    '''
    status_info = {}
    for int_key, int_status in _status.items():
        if int_status['linkStatus'] == 'connected':
            status_info.update({int_key: [int_status['linkStatus'], int_status['description']]})

    return returnIntfList(status_info)

#----------------------------------------------------------------

def printList(lStatus):
    print'#--Interface--#\t\t#--Status--#\t\t#--Description--#'
    for value in lStatus:
        print value

#----------------------------------------------------------------


def main():
    '''Run only if program called by itself'''
    switch = arista()
    status = switch.runCmd()
    printList(getDisabledIntf(status))
    print '\n'
    printList(getConnectedIntf(status))
 
 
if __name__ == '__main__':
    main()
