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
BINLOG_EVENT_FLAGS_BYTES = 2

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

    def timestamp(self):
        return self.__timestamp

    def event_type(self):
        return self.__event_type

    def server_id(self):
        return self.__server_id

    def event_size(self):
        return self.__event_size

    def log_pos(self):
        return self.__log_pos

    def flags(self):
        return self.__flags

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

# 0x01
class BinlogStartEventV3:
    def __init__(self):
        self.__binlog_version = 0       # 2 bytes
        self.__mysql_server_version = ''    # 50 bytes
        self.__create_timestamp = 0         # 4 bytes

    def binlog_version(self):
        return self.__binlog_version

    def mysql_server_version(self):
        return self.__mysql_server_version

    def create_timestamp(self):
        return self.__create_timestamp

    def parse(self, data):
        offset = 0
        self.__binlog_version = Utils.str2int(data[offset : ], 2)
        offset += 2
        self.__mysql_server_version = data[offset : offset + 50]
        offset += 50
        self.__create_timestamp = Utils.str2int(data[offset : ], 4)

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

# 0x02
class BinlogQueryEvent:
    def __init__(self):
        self.__slave_proxy_id = 0       # 4 bytes
        self.__execution_time = 0       # 4 bytes
        self.__schema_length = 0        # 1 byte
        self.__error_code = 0           # 2 bytes
        self.__status_vars_length = 0   # 2 bytes
        self.__status_vars = ''         # status_vars_length bytes
        self.__schema = ''              # schema_length bytes
        self.__reserved = 0             # 1 byte
        self.__query = ''               # EOF

    def slave_proxy_id(self):
        return  self.__slave_proxy_id

    def execution_time(self):
        return self.__execution_time

    def schema_length(self):
        return self.__schema_length

    def error_code(self):
        return self.__error_code

    def status_vars_length(self):
        return self.__status_vars_length

    def status_vars(self):
        return self.__status_vars

    def schema(self):
        return self.__schema

    def query(self):
        return  self.__query

    def parse(self, data):
        offset = 0
        self.__slave_proxy_id = Utils.str2int(data[offset : ], 4)
        offset += 4
        self.__execution_time = Utils.str2int(data[offset : ], 4)
        offset += 4
        self.__schema_length = Utils.str2int(data[offset : ], 1)
        offset += 1
        self.__error_code = Utils.str2int(data[offset : ], 2)
        offset += 2
        self.__status_vars_length = Utils.str2int(data[offset : ], 2)
        offset += 2
        self.__status_vars = data[offset : offset + self.__status_vars_length]
        offset += self.__status_vars_length
        self.__schema = data[offset : offset + self.__schema_length]
        offset += self.__schema_length
        self.__reserved = Utils.str2int(data[offset : ], 1)
        offset += 1
        self.__query = data[offset : ]
        print b2a_hex(self.__status_vars)

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

# 0x03
class BinlogStopEvent:
    def __init__(self):
        pass

    def parse(self, data):
        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

# 0x04
class BinlogRotateEvent:
    def __init__(self):
        self.__position = 0         # 8 byts
        self.__next_binlog = ''     #

    def position(self):
        return self.__position;

    def next_binlog(self):
        return self.__next_binlog;

    def parse(self, data):
        offset = 0
        self.__position = Utils.str2int(data[offset : ], 8)
        offset += 8
        self.__next_binlog = data[offset : ]

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

# 0x05
class BinlogIntvarEvent:
    def __init__(self):
        self.__type = 0     # 1 byte
        self.__value = 0    # 8 bytes

    def type(self):
        return self.__type

    def value(self):
        return self.__value

    def parse(self, data):
        offset = 0
        self.__type = Utils.str2int(data[offset : ], 1)
        offset += 1
        self.__value = Utils.str2int(data[offset : ], 8)

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value
# 0x0F
class BinlogFormatDescriptionEvent:
    def __init__(self):
        self.__binlog_version = 0   # 2 bytes
        self.__mysql_server_version = ''    # 50 bytes
        self.__create_timestamp = 0     # 4 bytes
        self.__event_header_length = 0  # 1 byte
        self.__event_type_header_lengths = ''

    def binlog_version(self):
        return self.__binlog_version

    def mysql_server_version(self):
        return self.__mysql_server_version

    def create_timestamp(self):
        return self.__create_timestamp

    def event_header_length(self):
        return self.__event_header_length

    def event_type_header_lengths(self):
        return self.__event_type_header_lengths

    def parse(self, data):
        offset = 0
        self.__binlog_version = Utils.str2int(data[offset : ], 2)
        offset += 2
        self.__mysql_server_version = data[offset : offset + 50]
        offset += 50
        self.__create_timestamp = Utils.str2int(data[offset : ], 4)
        offset += 4
        self.__event_header_length = Utils.str2int(data[offset : ], 1)
        offset += 1
        self.__event_type_header_lengths = data[offset : ]

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value
# 0x10
class BinlogXIDEvent:
    def __init__(self):
        self.__xid = 0

    def xid(self):
        return self.__xid

    def parse(self, data):
        self.__xid = Utils.str2int(data, 8)
        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

# 0x13
class BinlogTableMapEvent:
    def __init__(self):
        self.__table_id
class BinlogEvent:
    def __init__(self):
        self.__event_stat = 0
        self.__header = BinlogEventHeader()
        self.__event_body = None

    def header(self):
        return self.__header

    def event_body(self):
        return self.__event_body

    def event_status(self):
        return self.__event_stat

    def parse(self, data):
        offset = 0
        self.__event_stat = Utils.str2int(data, 1)
        offset += 1
        header = data[offset:]
        (data, passed) = self.__header.parse(header)
        offset += passed

        if self.__header.event_type() == Constants.BINLOG_START_EVENT_V3:
            self.__event_body = BinlogStartEventV3()
        elif self.__header.event_type() == Constants.BINLOG_QUERY_EVENT:
            self.__event_body = BinlogQueryEvent()
        elif  self.__header.event_type() == Constants.BINLOG_ROTATE_EVENT:
            self.__event_body = BinlogRotateEvent()
        elif self.__header.event_type() == Constants.BINLOG_FORMAT_DESCRIPTION_EVENT:
            self.__event_body = BinlogFormatDescriptionEvent()
        elif self.__header.event_type() == Constants.BINLOG_XID_EVENT:
            self.__event_body = BinlogXIDEvent()
        else:
            pass

        if self.__event_body != None:
            self.__event_body.parse(data)
            self.__event_body.dump()

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value
