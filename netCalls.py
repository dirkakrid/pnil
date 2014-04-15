#!/usr/bin/env python

'''Module to test calls to eapLib'''

#----------------------------------------------------------------

from pnil.lib.netControl import netDevice
from pnil.lib.netView import printResult
from pnil.utils.tools import initArgs
from pnil.utils.findRoutes import standardRoutes

#----------------------------------------------------------------

# -------------------
# GLOBAL VARIABLES FOR PRINTING AND RUNNING
# -------------------
ARISTA = True
CISCO_IOS = False
USE_ARGS = True
# -------------------

def main():
    '''
    Ran only if program called as script
    '''
    if ARISTA and USE_ARGS == True:
        sw1 = netDevice(USE_ARGS)
        result = sw1.run()

        printResult(result)


    if ARISTA and USE_ARGS == False:
        sw1 = netDevice()
        sw1.initialize('veos-01', 'arista', 'sw1')
        sw1.setLogin('arista', 'arista')
        # # function = 'getHostname, getVersion, getPlatform, getCPU, getDetails'
        function = 'getDetails'
        kargs = {'vrf': None, 'options': None}
        # result = sw1.run(function)
        result = sw1.run(function, kargs)

        printResult(result)


    # Till I figure out the paramiko exception, raw data input
    if CISCO_IOS:
        pass


if __name__ == '__main__':
    main()
