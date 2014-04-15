### Python Network Interface Library

Author:             [@IPYandy](https://twitter.com/IPyandy) (Yandy Ramirez)
Code Verion:    	0.0.1
Reason:             Because I can!

### Python Dependencies

Code runs only on Python 2.7, to be more specific Python > 2.7.2 < 3.X

# Module Dependencies

* jsonrpclib
* re, shlex
* itertools
* pprint 
	* optional for displaying dictionaries and lists a bit nicer

Most of these are from the standard library, the only one that needs to be installed manually is **jsonrpclib**.

```shell
pip install jsonrpclib
```

Other dependencies will be updated as the library expands.

### Using the Library

As of this time, while some of the code would work on Cisco devices, the API calls only work on 


**Sample Call**
```bash
$ ./netCalls.py -n sw01 -m arista -i veos-01 -f getDetails
vendor:         arista
platform:       vEOS
version:        4.12.1-1581426.vEOS4125.1 (engineering build)
cpu_utilization:    Cpu(s):  6.8%us
total_sytem_memory:     1000444
serial_number:      12345
free_system_memory:     59700
hostname:       vEOS-1
connect_ip:         veos-01
system_uptime:      4 days
```

This code needs documentation, I know, working on it. :)

Follow my [BLOG](http://ipyandy.net) for more on networking, coding and rants.
Follow me on [Twitter @IPyandy](http://twitter.com/IPyandy) and stay in touch.

To be updated soon