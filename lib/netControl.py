import argparse
from eapiLib.utils.utils import checkIP
from eapiLib.lib.arista-eapi import arista-eapi
import pprint

class netDevice(object):
    """
        Parent class switch, which other classes will inherit from,
        ie. arista, cisco, juniper and so on
    """
    def __init__(self):
        super(Switch, self).__init__()
        # defaults for now, building methods
        self._net_device = None
        self._args = None
        self._initArgs()
        self._createNetDevice()

    def _initArgs(self):
        parser = argparse.ArgumentParser(description='\
            input -f [function] -i [ipAddress] \
            -u [username] -p [password]')

        parser.add_argument('-f', '--function', help='i.e. -f showIntfStatus, show version')
        parser.add_argument('-c', '--cli', help='i.e. same as -f, for redundancy')
        parser.add_argument('-i', '--ip_address', help='i.e. -i "192.168.31.21"')
        parser.add_argument('-u', '--username', help='Enter username of device')
        parser.add_argument('-p', '--password', help='Enter password for username')
        self._args = vars(parser.parse_args())

    # initialize command line arguments
    def _createNetDevice(self):
        pass

    # decides which method to run based on self._cli
    # methods can also be called directly, but this simplifies it to the "caller"
    # by only needing to know one function or the cli command to to call.
    def getCMD(self):
        '''
        Checks IMPLEMENTED_METHODS constant and tests if library has called method.
        otherwise terminates with mothod not implemented.
        '''
        implemented_methods = dir(Switch)
        print implemented_methods
        if self._cli not in implemented_methods:
            pp = pprint.PrettyPrinter(indent=4)
            print ('Choose from the following methods\n')
            pp.pprint(implemented_methods)
            raise ValueError('Error, no method with that name')

        else:
            # getattr uses a string and passes as function call
            return getattr(self, self._cli)()
