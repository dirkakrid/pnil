#!/usr/bin/env python

import pprint

def PrintResult(result, manufacturer='Arista'):
    pp = pprint.PrettyPrinter(indent=2, width=30)
    if type(result) is not str and type(result) is not unicode:
        print ('# ' + '-' * 80)
        print ('# {0} DATASTRUCTURE REPRESENTATION'.format(manufacturer.upper()))
        print ('# ' + '-' * 80 + '\n')
        pp.pprint(result)
        print ('\n# ' + '-' * 80 + '\n')
    else:
        print ('# ' + '-' * 80 + '\n')
        print (result)
        print ('\n# ' + '-' * 80 + '\n')
