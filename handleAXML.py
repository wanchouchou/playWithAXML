#!/usr/bin/python2.7
# FileName: handleAXML.py
# Author: wanchouchou
# mail: 200802376@qq.com
# Created Time: 2014-12-15

import os
import sys

import extendStringChunk
import utf_16
import options

def confuseAXML(AXML_inpath, AXML_outpath):
    #firstly, extend the string chunk for our DIY replace_attrName
    extendStringChunk.extend_AXML_stringChunk(AXML_inpath, AXML_outpath)
    #and then begin the operator of replacing. NOTE: currently, I just support the UTF-16.
    utf_16.replace_attrName(AXML_inpath, AXML_outpath)

def ambiguityAXML(AXML_inpath, AXML_outpath):
    CMD_MODIFY = './manifestAmbiguity -m ' + AXML_inpath + '  -o ' + AXML_outpath
    os.system(CMD_MODIFY)
    print 'Ambiguity Modify OK!'

def handle_AXML(argv):
    options_ret = options.handle_options(argv)
    if options_ret == 0 :
        sys.exit(1)
    
    CMD_RMDIR = 'rm -rf out *new.apk'
    CMD_MAKEDIR = 'mkdir -p out'
    CMD_UNZIP = 'unzip ' + options.opts_struct.source_filepath + ' -d out' 
    os.system(CMD_RMDIR)
    os.system(CMD_MAKEDIR)
    os.system(CMD_UNZIP)
    
    AXML_PATH = 'out' + os.sep + 'AndroidManifest.xml'
    if options.opts_struct.needConfuse == 1:
        confuseAXML(AXML_PATH, AXML_PATH)
    if options.opts_struct.needAmbiguity == 1:
        ambiguityAXML(AXML_PATH, AXML_PATH)
    
    os.system('./zipApk.sh')


    

handle_AXML(sys.argv[1 : ])

