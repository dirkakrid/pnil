#!/usr/bin/env python

'''Module to test calls to eapLib'''

#----------------------------------------------------------------

from pnil.lib.control.netControl import netDevice
from pnil.lib.view.netView import printResult

#----------------------------------------------------------------

# -------------------
# GLOBAL VARIABLES FOR PRINTING AND RUNNING
# -------------------
MANUFACTURER = 'ARISTA'
USE_ARGS = True
# -------------------

def main():
    '''
    Ran only if program called as script
    '''
    if USE_ARGS == True:
        sw1 = netDevice(USE_ARGS)
        result = sw1.run()

        printResult(result, sw1.getManufacturer())


    elif MANUFACTURER == 'ARISTA':
        sw1 = netDevice()
        sw1.initialize('veos-01', 'arista', 'sw1')
        sw1.setLogin('arista', 'arista')
        # # function = 'getHostname, getVersion, getPlatform, getCPU, getDetails'
        function = 'getRoutes'
        kargs = {'vrf': None, 'options': None}
        # result = sw1.run(function)
        result = sw1.run(function, kargs)

        printResult(result)


    elif MANUFACTURER == 'CISCO':
        cisco1 = netDevice()
        cisco1.initialize('csr1kv-01', 'cisco', 'cisco1')
        cisco1.setLogin('cisco', 'cisco')
        function = 'getDetails'
        kargs = {'vrf': None, 'options': None}
        result = cisco1.run(function)
        # result = cisco1.run(function, kargs)

        printResult(result)


if __name__ == '__main__':
    main()
