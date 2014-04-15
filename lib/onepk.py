#!/usr/bin/env python


import sys
if sys.version_info > (2, 7, 2) and sys.version_info < (3, 0):

    from configobj import ConfigObj
    # from datetime import datetime
    # import json

    # from onep.element.NetworkElement import NetworkApplication, NetworkElement
    # from onep.interfaces.InterfaceStatus import InterfaceStatus
    from onep.interfaces.InterfaceFilter import InterfaceFilter
    # from onep.interfaces.InterfaceConfig import InterfaceConfig
    from onep.element.SessionConfig import SessionConfig
    # from onep.interfaces import NetworkInterface
    from onep.core.exception import OnepDuplicateElementException
    from onep.vty.VtyService import VtyService
    # from onep.cdp.CDPListener import CDPListener
    # from onep.cdp.CDPEvent import CDPEvent
    # from onep.cdp.CDPFilter import CDPFilter
    # from onep.routing.RIB import RIB
    from onep.routing.RoutingClass import Routing
    from onep.routing.L3UnicastRIBFilter import L3UnicastRIBFilter
    from onep.routing.L3UnicastScope import L3UnicastScope
    from onep.routing.L3UnicastRouteRange import L3UnicastRouteRange
    from onep.interfaces.NetworkPrefix import NetworkPrefix
    from onep.routing.RouteRange import RouteRange

    class onepk(object):
        def __init__(self):
            super(onepk, self).__init__()
            self._host = None
            self._user = 'cisco'
            self._pass = 'cisco'
            self._device = None
            self._name = None
            self._version_info = None
            self._connected = False

        def connect(self):

            session_config = SessionConfig(
            SessionConfig.SessionTransportMode.TLS)
            session_config.ca_certs = "/usr/local/certs/csr1kv-01.pem"
            ne = self.myapp.get_network_element(self._host)

            if not ne.is_connected():
                try:
                    session_handle = ne.connect(
                        self._user, self._pass, session_config)
                except OnepDuplicateElementException, e:
                    # print e
                    existing = e.get_original_network_element()
                    # print existing
                    print ('Unable to connect to device.')
                except Exception, e:
                    # print e
                    print('Could not connect to  {0} Please validate reachability.'.format(self._host))
                    return 'DNE'
            else:
                print('Connection to {0} already exists, but you can use this new \
                    object if you want.'.format(self._host))

            return ne

        def setLogin(self, username, password):
            self._user = username
            self._pass = password

        def getserialNumber(self):
            return self._device.properties.SerialNo

        def getCPU(self):
            return self._device.system_cpu_utilization

        def getfreeMemory(self):
            return self._device.get_free_system_memory()

        def gettotalMemory(self):
            return self._device.total_system_memory

        def getHostname(self):
            return self._device.properties.sys_name

        def getUptime(self):
            return self._device.properties.sys_uptime

        def getPlatform(self):
            return self._device.properties.product_id

        def getReasonforReboot(self):
            reason = 'Unknown'
            vty_session = VtyService(self._device)
            vty_session.open()
            parsed_show_version = vty_session.write(
                'show version').split('\n')
            for line in parsed_show_version:
                if line.startswith('Last reload'):
                    parsed_line = line.split(':')
                    reason = parsed_line[1].strip()
                    return reason
            vty_session.close()

        def useCLI(self, command):
            vty_session = VtyService(self._device)
            vty_session.open()
            parsed_show = vty_session.write(command)
            # print parsed_showd
            vty_session.close()
            return parsed_show

        def getInterfaces(self):
            ifilter = InterfaceFilter()
            return self._device.get_interface_dict(ifilter).keys()

        def getInterfaceDetail(self):
            ifilter = InterfaceFilter()
            inter = self._device.get_interface_dict(ifilter).keys()
            inter_dict = {}

            for i in inter:

                config = self._device.get_interface_by_name(i).get_config()
                vrf = self._device.get_interface_by_name(i).get_vrf_name()
                inter_dict[
                    i] = {'mac_address': config.mac_address, 'mtu': config.mtu, 'vrf': vrf,
                          'description': config.description, 'rx_bandwith': config.rx_bandwidth,
                          'tx_bandwidth': config.tx_bandwidth}
            return inter_dict

        def d(self):
            self._device.disconnect()

        def getRoutes(self):

            # currently need to fix this function

            routing = Routing.get_instance(self._device)
            #rib = routing.rib
            scope = L3UnicastScope()
            rib_filter = L3UnicastRIBFilter()
            prefix = NetworkPrefix('0.0.0.0', 0)
            count = 20
            range1 = L3UnicastRouteRange(
                prefix, RouteRange.RangeType.EQUAL_OR_LARGER, count)
            route_list = routing.rib.get_route_list(
                scope, rib_filter, range1)

            routes = {}
            all_routes = {}
            c = 1
            for r in route_list:
                routes['route'] = str(r.prefix.address) + \
                    '/' + str(r.prefix.prefix_length)
                routes['prefix'] = r.prefix.address
                routes['prefix_length'] = r.prefix.prefix_length
                routes['admin_distance'] = r.admin_distance
                routes['type'] = ''
                routes['metric'] = ''
                all_routes[c] = routes
                # print json.dumps(routes,indent=5)

            return all_routes

        def getDetails(self):
            cpu_utilization = self.getCPU()
            free_memory = self.getfreeMemory()
            total_memory = self.gettotalMemory()
            hostname = self.getHostname()
            uptime = self.getUptime()
            platform = self.getPlatform()
            serial_number = self.getserialNumber()
            reboot_reason = self.getReasonforReboot()
            connect_ip = self._host
            interfaces = self.getInterfaces()

            facts = {
                'connect_ip': connect_ip, 'serial_number': serial_number, 'cpu_utilization': cpu_utilization, 'free_system_memory': free_memory,
                'total_sytem_memory': total_memory, 'hostname': hostname, 'system_uptime': uptime, 'platform': platform,
                'last_reboot_reason': reboot_reason, 'vendor': 'cisco', 'interfaces': interfaces, 'var_name': self._name}

            config = ConfigObj(
                '/home/cisco/apps/cpal/core/device_tags.ini').dict()
            for key in config.keys():
                if key == self._host:
                    facts.update(config[key])
            return facts

else:
    raise ValueError(
        "Only version greater than 2.7 and less then 3.0 are supported")
