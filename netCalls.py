#!/usr/bin/env python

'''Module to test calls to eapLib'''

#----------------------------------------------------------------

from lib.control.NetControl import NetDevice
from lib.view.NetworkView import PrintResult

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
    if USE_ARGS:
        dev1 = NetDevice(USE_ARGS)
        result = dev1.run()

        PrintResult(result, dev1.getManufacturer())


    elif MANUFACTURER == 'ARISTA':
        sw1 = NetDevice()
        sw1.initialize('veos-01', 'arista', 'sw1')
        sw1.setLogin('arista', 'arista')
        # # function = 'getHostname, getVersion, getPlatform, getCPU, getDetails'
        function = 'getRoutes'
        kargs = {'vrf': None, 'options': None}
        # result = sw1.run(function)
        result = sw1.run(function, kargs)

        PrintResult(result)


    elif MANUFACTURER == 'CISCO':
        cisco1 = NetDevice()
        cisco1.initialize('csr1kv-01', 'cisco', 'cisco1')
        cisco1.setLogin('cisco', 'cisco')
        function = 'getDetails'
        kargs = {'vrf': None, 'options': None}
        result = cisco1.run(function)
        # result = cisco1.run(function, kargs)

        PrintResult(result)


if __name__ == '__main__':
    main()
