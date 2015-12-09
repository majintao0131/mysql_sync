#!/usr/bin/env python
__author__ = 'jintao'

from Utils import Utils
from binascii import b2a_hex, a2b_hex
import Constants

class BinlogEventHeader:
    def __init__(self):
        self.__timestamp = 0            # 4 bytes
        self.__event_type = 0           # 1 byte
        self.__server_id = 0            # 4 bytes
        self.__event_size = 0           # 4 bytes
        self.__log_pos = 0              # 4 bytes
        self.__flags = 0                # 2 bytes

    def parse(self, data):
        offset = 0
        self.__timestamp = Utils.str2int(data[offset:], 4)
        offset += 4
        self.__event_type = Utils.str2int(data[offset:], 1)
        offset += 1
        self.__server_id = Utils.str2int(data[offset:], 4)
        offset += 4
        self.__event_size = Utils.str2int(data[offset:], 4)
        offset += 4
        self.__log_pos = Utils.str2int(data[offset:], 4)
        offset += 4
        self.__flags = Utils.str2int(data[offset:], 2)
        offset += 2

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

class BinlogStatusVars:
    def __init__(self):
        self.__code = 0
        self.__value = 0

    def parse(self, data):
        offset = 0
        self.__code = Utils.str2int(data[offset : ], 1)
        offset += 1
        if self.__code == Constants.Q_FLAGS2_CODE \
                or self.__code == Constants.Q_MASTER_DATA_WRITTEN_CODE:
            self.__value = Utils.str2int(data[offset : ], 4)
            offset += 4
        elif self.__code == Constants.Q_SQL_MODE_CODE \
                or self.__code == Constants.Q_TABLE_MAP_FOR_UPDATE_CODE:
            self.__value = Utils.str2int(data[offset : ], 8)
            offset += 8
        elif self.__code == Constants.Q_CATALOG:
            length = Utils.str2int(data[offset : ], 1)
            offset += 1
            self.__value  = data[offset : offset + length] + '\0'
            offset += length
        elif self.__code == Constants.Q_AUTO_INCREMENT:
            increment = Utils.str2int(data[offset : ], 2)
            offset += 2
            inc_offset = Utils.str2int(data[offset : ], 2)
            offset += 2
            self.__value = (increment, inc_offset)
        elif self.__code == Constants.Q_CHARSET_CODE:
            client_ch = Utils.str2int(data[offset : ], 2)
            offset += 2
            col_conn = Utils.str2int(data[offset : ], 2)
            offset += 2
            coll_server = Utils.str2int(data[offset : ], 2)
            offset += 2
            self.__value = (client_ch, col_conn, coll_server)
        elif self.__code == Constants.Q_TIME_ZONE_CODE:
            length = Utils.str2int(data[offset : ], 1)
            offset += 1
            self.__value = data[offset : offset + length]
            offset += length
        elif self.__code == Constants.Q_CATALOG_NZ_CODE:
            length = Utils.str2int(data[offset : ], 1)
            offset += 1
            self.__value = data[offset : offset + length]
            offset += length
        elif self.__code == Constants.Q_LC_TIME_NAMES_CODE \
            or self.__code == Constants.Q_CHARSET_DATABASE_CODE:
            self.__value = Utils.str2int(data[offset : ], 2)
            offset += 2
        elif self.__code == Constants.Q_INVOKERS:
            length = Utils.str2int(data[offset : ], 1)
            offset += 1
            username = data[offset : offset + length]
            offset += length
            length = Utils.str2int(data[offset : ], 1)
            offset += 1
            hostname = data[offset : offset : length]
            offset += length
            self.__value = (username, hostname)
        elif self.__code == Constants.Q_UPDATED_DB_NAMES:
            count = Utils.str2int(data[offset : ], 1)
            offset += 1
            terms = []
            for i in range(count):
                pos = data.find('\0', offset)
                terms.append(data[offset : offset + pos + 1])
                offset += (pos + 1)
            self.__value = (count, terms)
        elif self.__code == Constants.Q_MICROSECONDS:
            self.__value = Utils.str2int(data[offset : ], 3)
            offset += 3
        return (self.__code, self.__value, offset)

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
        self.__status_vars = {}         # status_vars_length bytes
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
        end_pos = offset + self.__status_vars_length
        while offset < end_pos:
            vars = BinlogStatusVars()
            (key, value, off) = vars.parse(data[offset : ])
            self.__status_vars[key] = value
            offset += off

        self.__schema = data[offset : offset + self.__schema_length]
        offset += self.__schema_length
        self.__reserved = Utils.str2int(data[offset : ], 1)
        offset += 1
        self.__query = data[offset : ]

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
        self.__next_binlog = ''     # EOF

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
        self.__event_type_header_lengths = []

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
        end_pos = len(data)
        while offset < end_pos:
            self.__event_type_header_lengths.append(Utils.str2int(data[offset : ], 1))
            offset += 1
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

class BinlogLoadQueryEvent:
    def __init__(self):
        self.__slave_proxy_id = 0       # 4 bytes
        self.__execution_time = 0       # 4 bytes
        self.__schema_length = 0        # 1 byte
        self.__error_code = 0           # 2 bytes
        self.__status_vars_length = 0   # 2 bytes
        self.__file_id = 0              # 4 bytes
        self.__start_pos = 0            # 4 bytes
        self.__end_pos = 0              # 4 bytes
        self.__dup_handling_flags = 0   # 1 byte

    def slave_proxy_id(self):
        return self.__slave_proxy_id

    def execution_time(self):
        return self.__execution_time

    def schema_length(self):
        return self.__schema_length

    def error_code(self):
        return self.__error_code

    def status_vars_length(self):
        return self.__status_vars_length

    def file_id(self):
        return self.__file_id

    def start_pos(self):
        return self.__start_pos

    def end_pos(self):
        return self.__end_pos

    def dup_handling_flags(self):
        return self.__dup_handling_flags

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
        self.__file_id = Utils.str2int(data[offset : ], 4)
        offset += 4
        self.__start_pos = Utils.str2int(data[offset : ], 4)
        offset += 4
        self.__end_pos = Utils.str2int(data[offset : ], 4)
        offset += 4
        self.__dup_handling_flags = Utils.str2int(data[offset : ], 1)
        offset += 1
        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

# 0x13
class BinlogTableMapEvent:
    def __init__(self):
        self.__table_id = 0             # 6 bytes
        self.__flags = 0                # 2 bytes
        self.__schema_name_length = 0   # 1 byte
        self.__schema_name = ''         # schema_name_length bytes
        self.__reserver1 = 0x00         # 1 byte
        self.__table_name_length = 0x00 # 1 byte
        self.__table_name = ''          # table_name_length bytes
        self.__reserver2 = 0x00         # 1 byte
        self.__column_count = 0         # lenenc bytes
        self.__column_def = []          # column_count bytes
        self.__column_meta_def_length = 0   # lenenc byte
        self.__column_meta_def = []      # column_meta_def_length bytes
        self.__null_bitmap = []          # (column_count + 8) / 7 bytes

    def table_id(self):
        return self.__table_id

    def flags(self):
        return self.__flags

    def schema_name_length(self):
        return self.__schema_name_length

    def schema_name(self):
        return self.__schema_name

    def table_name_length(self):
        return self.__table_name_length

    def table_name(self):
        return self.__table_name

    def column_count(self):
        return self.__column_count

    def column_def(self):
        return self.__column_def

    def column_meta_def(self):
        return self.__column_meta_def

    def null_bitmap(self):
        return self.__null_bitmap

    def parse(self, data):
        offset = 0
        self.__table_id = Utils.str2int(data[offset : ], 6)
        offset += 6
        self.__flags = Utils.str2int(data[offset : ], 2)
        offset += 2
        self.__schema_name_length = Utils.str2int(data[offset : ], 1)
        offset += 1
        self.__schema_name = data[offset : offset + self.__schema_name_length]
        offset += self.__schema_name_length
        self.__reserver1 = Utils.str2int(data[offset : ], 1)
        offset += 1
        self.__table_name_length = Utils.str2int(data[offset : ], 1)
        offset += 1
        self.__table_name = data[offset : offset + self.__table_name_length]
        offset += self.__table_name_length
        self.__reserver2 = Utils.str2int(data[offset : ], 1)
        offset += 1
        (self.__column_count, passed) = Utils.str2lenencint(data[offset : ])
        offset += passed
        for i in range(self.__column_count):
            self.__column_def.append(Utils.str2int(data[offset : ], 1))
            offset += 1

        (self.__column_meta_def_length, passed) = Utils.str2lenencint(data[offset : ])
        offset += passed
        for i in range(self.__column_meta_def_length):
            self.__column_meta_def.append(Utils.str2int(data[offset : ], 1))
            offset += 1
        bitmap_length = (self.__column_count + 8) / 7
        self.__null_bitmap = Utils.bit2list(Utils.str2int(data[offset : ], self.__column_count), self.__column_count)
        offset += bitmap_length
        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

class BinlogRowField:
    def __init__(self, type):
        self.__field_type = type
        self.__length = 0
        self.__value = None

    def field_type(self):
        return self.__field_type

    def length(self):
        return self.__length

    def value(self):
        return self.__value

    def parse(self, data):
        offset = 0
        if self.__field_type == Constants.MYSQL_TYPE_STRING \
            or self.__field_type == Constants.MYSQL_TYPE_VARCHAR \
            or self.__field_type == Constants.MYSQL_TYPE_VAR_STRING \
            or self.__field_type == Constants.MYSQL_TYPE_ENUM \
            or self.__field_type == Constants.MYSQL_TYPE_SET \
            or self.__field_type == Constants.MYSQL_TYPE_BLOB \
            or self.__field_type == Constants.MYSQL_TYPE_MEDIUM_BLOB \
            or self.__field_type == Constants.MYSQL_TYPE_LONG_BLOB \
            or self.__field_type == Constants.MYSQL_TYPE_TINY_BLOB \
            or self.__field_type == Constants.MYSQL_TYPE_GEOMETRY \
            or self.__field_type == Constants.MYSQL_TYPE_BIT \
            or self.__field_type == Constants.MYSQL_TYPE_DECIMAL \
            or self.__field_type == Constants.MYSQL_TYPE_NEWDECIMAL:
            (self.__length, passed) = Utils.str2lenencint(data[offset : ])
            offset += passed
            self.__value = data[offset : offset + self.__length]
            offset += self.__length
        elif self.__field_type == Constants.MYSQL_TYPE_LONGLONG:
            self.__length = 8
            self.__value = Utils.str2int(data[offset : ], self.__length)
            offset += self.__length
        elif self.__field_type == Constants.MYSQL_TYPE_LONG \
            or self.__field_type == Constants.MYSQL_TYPE_INT24:
            self.__length = 4
            self.__value = Utils.str2int(data[offset : ], self.__length)
            offset += self.__length
        elif self.__field_type == Constants.MYSQL_TYPE_SHORT \
            or self.__field_type == Constants.MYSQL_TYPE_YEAR:
            self.__length = 2
            self.__value = Utils.str2int(data[offset : ], self.__length)
            offset += self.__length
        elif self.__field_type == Constants.MYSQL_TYPE_TINY:
            self.__length = 1
            self.__value = Utils.str2int(data[offset : ], self.__length)
            offset += self.__length
        elif self.__field_type == Constants.MYSQL_TYPE_DOUBLE:
            self.__length = 8
            self.__value = Utils.str2double(data[offset : ], self.__length)
            offset += self.__length
        elif self.__field_type == Constants.MYSQL_TYPE_FLOAT:
            self.__length = 4
            self.__value = Utils.str2double(data[offset : ], self.__length)
            offset += self.__length
        elif self.__field_type == Constants.MYSQL_TYPE_DATETIME \
            or self.__field_type == Constants.MYSQL_TYPE_DATE \
            or self.__field_type == Constants.MYSQL_TYPE_TIMESTAMP:
            self.__length = Utils.str2int(data[offset : ], 1)
            offset += self.__length
        elif self.__field_type == Constants.MYSQL_TYPE_TIME:
            self.__length = Utils.str2int(data[offset : ], 1)
            offset += self.__length
        else:
            pass
        return offset

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

class BinlogRow:
    def __init__(self, binlog_event_manage, header, body):
        self.__binlog_event_manage = binlog_event_manage
        self.__header = header
        self.__body = body
        self.__nul_bitmap = []       # (bits set in 'columns-present-bitmap1'+7)/8
        self.__field_values = []      # nul-bitmap define the length
        self.__nul_bitmap2 = []       # (bits set in 'columns-present-bitmap2'+7)/8
        self.__field_values2 = []      # nul-bitmap2 define the length

    def nul_bitmap(self):
        return self.__nul_bitmap

    def field_values(self):
        return self.__field_values

    def nul_bitmap2(self):
        return self.__nul_bitmap2

    def field_values2(self):
        return self.__field_values2

    def parse(self, data):
        offset = 0
        table_map_event = self.__binlog_event_manage.last_table_map_event()
        bit_count = Utils.bitlist1count(self.__body.columns_present_bitmap1())
        self.__nul_bitmap = Utils.bit2list(Utils.str2int(data[offset : ], bit_count), bit_count)
        offset += (bit_count + 7)/8
        for i in range(self.__body.columns_number()):
            field = BinlogRowField(table_map_event.event_body().column_def()[i])
            if self.__nul_bitmap[i] == 0:
                offset += field.parse(data[offset : ])
                self.__field_values.append(field)
            else:
                self.__field_values.append(None)

        if self.__header.event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv1 \
                or self.__header.event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv2:
            bit_count = Utils.bitlist1count(self.__body.columns_present_bitmap2())
            self.__nul_bitmap2 = Utils.bit2list(Utils.str2int(data[offset : ], bit_count), bit_count)
            offset += (bit_count + 7)/8
            for i in range(self.__body.columns_number()):
                field = BinlogRowField(table_map_event.event_body().column_def()[i])
                if self.__nul_bitmap2[i] == 0:
                    offset += field.parse(data[offset : ])
                    self.__field_values2.append(field)
                else:
                    self.__field_values2.append(None)
        return offset

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

# 0x14 & 0x15 & 0x16 & 0x17 & 0x18 & 0x19 & 0x1e & 0x1f & 0x20
class BinlogRowEvent:
    def __init__(self, binlog_event_manage, header):
        self.__binlog_event_manage = binlog_event_manage
        self.__header = header
        self.__table_id = 0         # 6 bytes
        self.__flags = 0            # 2 bytes
        self.__extra_data_length = 0    # 2 bytes
        self.__extra_data = ''      # extra_data_length bytes
        self.__columns_number = 0   # lenenc bytes
        self.__columns_present_bitmap1 = []      # (columns_number+7)/8 bytes
        self.__columns_present_bitmap2 = []      # (columns_number+7)/8 bytes
        self.__rows = []

    def table_id(self):
        return self.__table_id

    def flags(self):
        return self.__flags

    def extra_data_length(self):
        return self.__extra_data_length

    def extra_data(self):
        return self.__extra_data

    def columns_number(self):
        return self.__columns_number

    def columns_present_bitmap1(self):
        return self.__columns_present_bitmap1

    def columns_present_bitmap2(self):
        return self.__columns_present_bitmap2

    def rows(self):
        return self.__rows

    def parse(self, data):
        offset = 0
        post_header_len = self.__binlog_event_manage.last_description_event().event_body().event_type_header_lengths()[self.__header.event_type() - 1]
        self.__table_id = Utils.str2int(data[offset : ], post_header_len - 2)
        offset += (post_header_len - 2)
        self.__flags = Utils.str2int(data[offset : ], 2)
        offset += 2

        if self.__header.event_type() == Constants.BINLOG_WRITE_ROWS_EVENTv2 \
            or self.__header.event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv2 \
            or self.__header.event_type() == Constants.BINLOG_DELETE_ROWS_EVENTv2:
            self.__extra_data_length = Utils.str2int(data[offset : ], 2)
            offset += 2
            self.__extra_data = data[offset : offset + self.__extra_data_length]
            offset += self.__extra_data_length

        (self.__columns_number, passed) = Utils.str2lenencint(data[offset : ])
        offset += passed
        bitmap_bytes = (self.__columns_number + 7) / 8
        self.__columns_present_bitmap1 = Utils.bit2list(Utils.str2int(data[offset : ], self.__columns_number), self.__columns_number)
        offset += bitmap_bytes

        if self.__header.event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv1 \
            or self.__header.event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv2:
            self.__columns_present_bitmap2 = Utils.bit2list(Utils.str2int(data[offset : ], self.__columns_number), self.__columns_number)
            offset += bitmap_bytes

        total_len = len(data)
        while offset < total_len:
            row = BinlogRow(self.__binlog_event_manage, self.__header, self)
            offset += row.parse(data[offset : ])
            self.__rows.append(row)

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

class BinlogEvent:
    def __init__(self, manage, used_index = None):
        self.__manage = manage
        self.__used_index = used_index
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
        self.__event_stat = Utils.str2int(data[offset : ], 1)
        offset += 1
        header = data[offset : ]
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
        elif self.__header.event_type() == Constants.BINLOG_EXECUTE_LOAD_QUERY_EVENT:
            self.__event_body = BinlogLoadQueryEvent()
        elif self.__header.event_type() == Constants.BINLOG_TABLE_MAP_EVENT:
            self.__event_body = BinlogTableMapEvent()
        elif self.__header.event_type() == Constants.BINLOG_WRITE_ROWS_EVENTv0 \
            or self.__header.event_type() == Constants.BINLOG_WRITE_ROWS_EVENTv1 \
            or self.__header.event_type() == Constants.BINLOG_WRITE_ROWS_EVENTv2 \
            or self.__header.event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv0 \
            or self.__header.event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv1 \
            or self.__header.event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv2 \
            or self.__header.event_type() == Constants.BINLOG_DELETE_ROWS_EVENTv0 \
            or self.__header.event_type() == Constants.BINLOG_DELETE_ROWS_EVENTv1 \
            or self.__header.event_type() == Constants.BINLOG_DELETE_ROWS_EVENTv2:
            self.__event_body = BinlogRowEvent(self.__manage, self.__header)
        else:
            print 'Cannt handle binlog event ' + str(self.__header.event_type())
            pass

        if self.__event_body != None:
            self.__event_body.parse(data)
            #self.__event_body.dump()

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

class BinlogEventManage:
    def __init__(self):
        self.__event_list = []
        self.__event_count = 0
        self.__last_table_map_event = None
        self.__last_description_event = None

    def last_table_map_event(self):
        return self.__last_table_map_event

    def last_description_event(self):
        return self.__last_description_event

    def append(self, data):
        binlog_event = BinlogEvent(self)
        binlog_event.parse(data)
        #binlog_event.header().dump()
        if binlog_event.header().event_type() == Constants.BINLOG_TABLE_MAP_EVENT:
            self.__last_table_map_event = binlog_event
        elif binlog_event.header().event_type() == Constants.BINLOG_FORMAT_DESCRIPTION_EVENT:
            self.__last_description_event = binlog_event

        self.__event_list.append(binlog_event)
        self.__event_count += 1

        return binlog_event

    def binlog_event(self, index):
        return self.__event_list[index]

    def event_count(self):
        return self.__event_count

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value