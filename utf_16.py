#!/usr/bin/python2.7
# FileName: utf-16.py
# Author: wanchouchou
# mail: 200802376@qq.com
# Created Time: 2014-12-12
import struct
import config 

def axmlUtf16Encode(string):
    bytes_str = bytearray(string.encode('utf-16'))
    len_str = len(string)
    pack_len_str = struct.pack('<I', len_str) 
    bytes_str[ : 2] = struct.unpack('BB', pack_len_str[ : 2])
    return bytes_str

def findUtf16InAXML(file_data, key_encoded, start_pos):
    pos = file_data.find(key_encoded, start_pos, -1)
    return pos

def replace_utf16(file_data, old_string, new_string):
    '''
    replace all old_string in the file_data with new_string
    '''
    new_string_encoded = axmlUtf16Encode(new_string)
    old_string_encoded = axmlUtf16Encode(old_string)
    n_s_e_len = len(new_string_encoded)
    o_s_e_len = len(old_string_encoded)
    
    pos = 0
    while True:
        pos = findUtf16InAXML(file_data, old_string_encoded, pos)
        if pos == -1:
            print 'In func(replace_utf16) replace old string \"%s\" over!' %old_string
            break
        #Start replace 
        file_data[pos : pos + n_s_e_len] = new_string_encoded[ : n_s_e_len]
    


def replace_attrName(source_AXML_name, dest_AXML_name):
        source_file = open(source_AXML_name, 'rb')
        file_data = bytearray(source_file.read())
        source_file.close()
        #new_string = '\n\n----######----\n------#-------\n-----#####----\n----#----#----\n---#-----#----\n--#-----##----\n\n'
        #old_string_list = ['label', 'theme', 'icon', 'minSdkVersion', 'versionCode', \
        #        'versionName', 'targetSdkVersion']
        new_string = config.NEW_STRING
	old_string_list = config.OLD_STRING_LIST
	for item in old_string_list:
            replace_utf16(file_data, item, new_string)

        f = open(dest_AXML_name, 'wb')
        f.write(file_data)
        f.close()
