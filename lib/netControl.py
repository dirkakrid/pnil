from eapiLib.utils.utils import checkIP, initArgs
from eapiLib.lib.eapi import eapi
import pprint

class netDevice(object):
    """
        Parent class switch, which other classes will inherit from,
        ie. arista, cisco, juniper and so on
    """
    def __init__(self):
        super(netDevice, self).__init__()
        # defaults for now, building methods
        self._args = initArgs()
        self.manufacturer = None
        self._ip_address = None
        self._api_call = None
        self._net_device = None
        self._createNetDevice()

    # creates the device self._net_device
    def _createNetDevice(self):
        if self._net_device.lower() == 'arista' or self._net_device.lower() == 'eapi':
            self._net_device = eapi()
        else:
            pass

    def initDevice(self):
        pass

    # decides which method to run based on self._apiCall
    # methods can also be called directly, but this simplifies it to the "caller"
    # by only needing to know one function or the cli command to to call.
    def getCMD(self):
        '''
        Checks IMPLEMENTED_METHODS constant and tests if library has called method.
        otherwise terminates with mothod not implemented.
        '''
        implemented_methods = dir(self._net_device)
        print implemented_methods
        if self._apiCall not in implemented_methods:
            pp = pprint.PrettyPrinter(indent=4)
            print ('Choose from the following methods\n')
            pp.pprint(implemented_methods)
            raise ValueError('Error, no method with that name')

        else:
            # getattr uses a string and passes as function call
            return getattr(self, self._apiCall)()
