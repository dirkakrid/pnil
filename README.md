### Python Network Interface Library

Author:             [@IPYandy](https://twitter.com/IPyandy) (Yandy Ramirez)
Code Verion:    None
Reason:             Because I can!

A fun little personal project using python to connect to network devices and do fun stuff. Not allot to show right now.


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

Any serious discovery or outcome that happens here, will probably be ported over to [CPAL](https://github.com/jedelman8/cpal). Which is a collaboration of a few engineers to standarize network device communication through APIs.

Follow my [BLOG](http://ipyandy.net) for more on networking, coding and rants.
Follow me on [Twitter @IPyandy](http://twitter.com/IPyandy) and stay in touch.

To be updated soon