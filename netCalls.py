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
ARGUMENTS = True
INTERPRETER_SIM = False if ARGUMENTS else True
# -------------------

def main():
    '''
    Ran only if program called as script
    '''
    if ARISTA and ARGUMENTS:
        args = initArgs()

        sw1 = netDevice(args)
        result = sw1.run(args)

        printResult(result)


    if ARISTA and INTERPRETER_SIM:
        sw1 = netDevice()
        sw1.initialize('veos-01', 'arista', 'sw1')
        sw1.setLogin('arista', 'arista')
        # # function = 'getHostname, getVersion, getPlatform, getCPU, getDetails'
        function = 'getRoutes'
        kargs = {'vrf': None, 'options': None}
        # result = sw1.run(function)
        result = sw1.run(function, kargs)

        printResult(result)


    # Till I figure out the paramiko exception, raw data input
    if CISCO_IOS:
        pass


if __name__ == '__main__':
    main()
