#!/usr/bin/python2.7
# FileName: options.py
# Author: wanchouchou
# mail: 200802376@qq.com
# Created Time: 2014-12-15

import sys
import getopt

class opts_struct:
    needAmbiguity = 0
    needConfuse = 0
    source_filepath = ''
    out_filepath = 'new.apk'

short_opts = 'haco:s:'
long_opts = ['help','ambiguity', 'confuse', 'out=','source=']


def useage():
    print '#############################################################'
    print 'Useage: '
    print '\t./handleAXML.py -s/--source=[Source.apk] -o/--out=[out.apk] '
    print '\t-c/--confuse  -m/--modify'
    print '##############################################################'

def handle_options(argv):
    global short_opts
    global long_opts
    
    try:
        opts, args = getopt.getopt(argv, short_opts, long_opts)
    except:
        print 'cmd formate error!'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            useage()
            return 0
        if opt in ('-a', '--ambiguity'):
            opts_struct.needAmbiguity = 1
        if opt in ('-c', '--confuse'):
            opts_struct.needConfuse = 1
        if opt in ('-s', '--source'):
            opts_struct.source_filepath = arg
        if opt in ('-o', '--out'):
            opts_struct.out_filepath = arg 

    return 1




