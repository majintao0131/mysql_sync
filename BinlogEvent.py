#!/usr/bin/env python
__author__ = 'jintao'

from Utils import Utils
from binascii import b2a_hex, a2b_hex
import Constants

BINLOG_EVENT_TIMESTAMP_BYTES = 4
BINLOG_EVENT_EVENTTYPE_BYTES = 1
BINLOG_EVENT_SERVERID_BYTES = 4
BINLOG_EVENT_SIZE_BYTES = 4
BINLOG_EVENT_LOGPOS_BYTES = 4
BINLOG_EVENT_FLAGS_BYTES = 4

class BinlogEventHeader:
    def __init__(self):
        self.__timestamp = 0            # 4 bytes
        self.__event_type = 0           # 1 byte
        self.__server_id = 0            # 4 bytes
        self.__event_size = 0           # 4 bytes
        self.__log_pos = 0              # 4 bytes
        self.__flags = 0                # 2 bytes

    def parse(self, data):
        global BINLOG_EVENT_TIMESTAMP_BYTES, \
            BINLOG_EVENT_EVENTTYPE_BYTES, \
            BINLOG_EVENT_SERVERID_BYTES, \
            BINLOG_EVENT_SIZE_BYTES, \
            BINLOG_EVENT_LOGPOS_BYTES, \
            BINLOG_EVENT_FLAGS_BYTES

        offset = 0
        self.__timestamp = Utils.str2int(data[offset:],BINLOG_EVENT_TIMESTAMP_BYTES)
        offset += BINLOG_EVENT_TIMESTAMP_BYTES
        self.__event_type = Utils.str2int(data[offset:], BINLOG_EVENT_EVENTTYPE_BYTES)
        offset += BINLOG_EVENT_EVENTTYPE_BYTES
        self.__server_id = Utils.str2int(data[offset:],BINLOG_EVENT_SERVERID_BYTES)
        offset += BINLOG_EVENT_SERVERID_BYTES
        self.__event_size = Utils.str2int(data[offset:], BINLOG_EVENT_SIZE_BYTES)
        offset += BINLOG_EVENT_SIZE_BYTES
        self.__log_pos = Utils.str2int(data[offset:], BINLOG_EVENT_LOGPOS_BYTES)
        offset += BINLOG_EVENT_LOGPOS_BYTES
        self.__flags = Utils.str2int(data[offset:], BINLOG_EVENT_FLAGS_BYTES)
        offset += BINLOG_EVENT_FLAGS_BYTES

        if len(data) > offset:
            return (data[offset:], offset)

        return ('', offset)

    def event_size(self):
        return self.__event_size

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

class BinlogEvent:
    def __init__(self):
        self.__event_stat = 0
        self.__header = BinlogEventHeader()

    def header(self):
        return self.__header

    def event_status(self):
        return self.__event_stat

    def parse(self, data):
        offset = 0
        self.__event_stat = Utils.str2int(data, 1)
        offset += 1
        header = data[offset:]
        if self.__event_stat == 0x00:
            (data, passed) = self.__header.parse(header)
            offset += passed
