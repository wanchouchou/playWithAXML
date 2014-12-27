#!/usr/bin/python2.7
# FileName: extendStringChunk.py
# Author: wanchouchou
# mail: 200802376@qq.com
# Created Time: 2014-12-14

import struct
import config

NEW_EACH_STRING_SIZE = config.NEW_EACH_STRING_SIZE

def getUint32(bytearray_data, pos):
    return struct.unpack_from('<I', bytearray_data[pos : pos + 4])[0]

def getUshort16(bytearray_data, pos):
    return struct.unpack_from('<H', bytearray_data[pos : pos + 2])[0]

def setUint32(bytearray_data, pos, uint):
    #first change the uint to streams
    tmp = struct.pack('<I', uint)
    bytearray_data[pos : pos + 4] = struct.unpack('BBBB', tmp[ : 4])

def cp_bytes(dest_data, source_data, len, pos_of_dest, pos_of_source):
    dest_data[pos_of_dest : pos_of_dest + len] = source_data[pos_of_source : pos_of_source + len]

def extend_and_copy_eachString(dest_data, source_data, \
        string_count, string_start_offset):
    global NEW_EACH_STRING_SIZE
    EXTEND_SIZE = 0  #record how many bytes the stringchunk added after we extended the stingchunk.
    #judge if the xml had been extended, throught calculating the distance between first and second string offset 
    first_string_offset = getUint32(source_data, 0x24)
    second_string_offset = getUint32(source_data, 0x24 + 4)
    need_extend = 0   
    if (second_string_offset - first_string_offset) < NEW_EACH_STRING_SIZE:
        need_extend = 1
        #debug 
        print 'need extend'
    else:
        print 'Do not need extend'

    for i in range(string_count):
        #firstly we need to extend each string to NEW_EACH_STRING_SIZE bytes
        old_value = getUint32(source_data, 0x24 + 4*i) #old_string_offset
        setUint32(dest_data, 0x24 + 4*i, NEW_EACH_STRING_SIZE * i)
        #and then copy all old_data to suitable location of dest_data
        cur_String_offset = string_start_offset + 0x8 + old_value
        cur_string_len = getUshort16(source_data, cur_String_offset)
        cur_string_bytes = 2 * (cur_string_len + 2)
        if need_extend == 1:
            EXTEND_SIZE += (NEW_EACH_STRING_SIZE - cur_string_bytes)
        pos_of_dest = string_start_offset + 0x8 + i * NEW_EACH_STRING_SIZE
        cp_bytes(dest_data, source_data, cur_string_bytes, pos_of_dest, cur_String_offset)
     

    return EXTEND_SIZE / 4 * 4  #NOTE!The last string in source_data maybe 4 aligned, so we mush offset it.

def extend_AXML_stringChunk(source_filename, target_filename):
        '''
        Open the AXML of source.apk defined by source_filename), and extend its stringchunk.
        At last, write the extended AXML to the file defined by target_filename.
        '''
        source_file = open(source_filename, 'rb')
        source_data = bytearray(source_file.read())
        source_file.close()
        dest_filename = target_filename
        dest_file = open(dest_filename, 'wb')
        #get filesize
        filesize = getUint32(source_data, 4)
        #get stringChunkSize
        string_chunk_size = getUint32(source_data, 0xc)
        #get count of strings
        string_count = getUint32(source_data, 0x10)
        #get string_start_offset
        string_start_offset = getUint32(source_data, 0x1c)
        print string_start_offset


        dest_data = bytearray(filesize * 20)
        dest_data[ : 0x24] = source_data[ : 0x24]
        EXTEND_SIZE = extend_and_copy_eachString(dest_data, source_data, string_count, string_start_offset)

        print filesize, EXTEND_SIZE

        source_resourceID_offset = 0x8 + string_chunk_size
        dest_resourceID_offset = source_resourceID_offset + EXTEND_SIZE
        #the last data should not be changed, so we copy them directly
        dest_data[dest_resourceID_offset : dest_resourceID_offset + filesize - source_resourceID_offset] = \
                source_data[source_resourceID_offset : filesize]

        #at last we should repair the filesize and stringChunkSize
        setUint32(dest_data, 4, filesize + EXTEND_SIZE)
        setUint32(dest_data, 0xc, string_chunk_size + EXTEND_SIZE)

        #write to the output file
        dest_file.write(dest_data[: filesize + EXTEND_SIZE])
        dest_file.close()

