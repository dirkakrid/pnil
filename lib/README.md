

### TODO ITEMS

* Find more efficient ways to parse text only output
    * Regex?
* Add more methods
    * Routes
    * LLDP Neighbors
    * arp table
    * class-maps
    * ...

#### The getHostname() Method

It now looks like this:

```python
def getHostname(self):
    ''' Returns the device's none FQDN hostname '''

    version_int = self._versionList()

    if int(version_int[0]) >= 4 and int(version_int[1]) >= 13:
        output = self._runCmd('show hostname')
        hostname = {'hostname': output[0]['hostname']}
        return hostname
    else:
        # begins a breakdown of finding the hostname inside a string
        # could probably be more efficient, but works for now
        output = self._switch.runCmds(1, ['show lldp local-info'], 'text')

        # gets the 4th line of output which contains the hostname in FQDN format
        host_line = output[0]['output'].split('\n')[3]

        # splits the line into a list at the delimeter and assigns the 2nd indext to fqdn
        # 2nd index contains the hostname
        host_fqdn = host_line.split(':')[1]

        # assignes the first index of fqdn after splitting at the delimeter (.)
        # this splits the fqdn into three parts, the [hostname, domain, suffix]
        hostname = host_fqdn.split('.')[0]
        hostname = hostname[2:]
        r_hostname = {'hostname': hostname}

        # indexing removes the " from the begining of the hostname
        return r_hostname
```

This can probably be cut down to a few lines after the first else: statement by using regex.