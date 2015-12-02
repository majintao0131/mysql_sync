#!/usr/bin/env python
__author__ = 'jintao'

from binascii import b2a_hex, a2b_hex
import sys
import Constants
from Utils import Utils

RESPONSE_PACKET_HEADER_BYTES = 1
RESPONSE_PACKET_WARNING_BYTES = 2
RESPONSE_PACKET_STATUSFLAGS_BYTES = 2
RESPONSE_PACKET_ERRORCODE_BYTES = 2
RESPONSE_PACKET_SQLSTATEMARKER_BYTES = 1
RESPONSE_PACKET_SQLSTATE_BYTES = 5


class ServerHandShakeMessage:
    def __init__(self):
        self.__offset = 0
        self.__length = 0

        self.__protocol_version = 0       # 1 byte
        self.__service_version = ""       # n bytes
        self.__connection_id = 0             # 4 bytes
        self.__auth_plugin_data = 0    # 20+ bytes
        self.__keep_field1 = 0            # 1 byte
        self.__capabilities_flags = 0      # 4 bytes
        self.__character_set = 0            # 1 byte
        self.__status_flags = 0           # 2 bytes
        self.__auth_plugin_data_len = 0   # 1 byte
        self.__keep_field2 = 0            # 10 bytes
        self.__auth_plugin_name = ''           # n bytes

    def offset(self):
        return self.__offset

    def length(self):
        return self.__length

    def protocol_version(self):
        return self.__protocol_version

    def connection_id(self):
        return self.__connection_id

    def auth_plugin_data(self):
        return self.__auth_plugin_data

    def keep_field1(self):
        return self.__keep_field1

    def capabilities_flags(self):
        return self.__capabilities_flags

    def character_set(self):
        return self.__character_set

    def status_flags(self):
        return self.__status_flags

    def auth_plugin_data_len(self):
        return self.__auth_plugin_data_len

    def keep_field2(self):
        return self.__keep_field2

    def auth_plugin_name(self):
        return self.__auth_plugin_name

    def parse_bytes(self, data, byte_count):
        res = b2a_hex(data[self.__offset : self.__offset + byte_count])
        self.__offset += byte_count
        return res

    def parse_int(self, data, byte_count):
        res = Utils.hex2int(b2a_hex(data[self.__offset : self.__offset + byte_count]), byte_count)
        self.__offset += byte_count
        return res

    def parse_string_by_count(self, data, byte_count):
        res = data[self.__offset : self.__offset + byte_count]
        self.__offset += byte_count
        return res

    def parse_string_by_split(self, data, split_flags):
        byte_count = data.find(split_flags, self.__offset) + 1 - self.__offset
        if byte_count < 0:
            byte_count = self
        return self.parse_string_by_count(data, byte_count)

    def parse(self, length, data):
        self.__length = length
        self.__protocol_version = self.parse_int(data, 1)
        self.__service_version = self.parse_string_by_split(data, '\x00')
        self.__connection_id = self.parse_int(data, 4)
        self.__auth_plugin_data = self.parse_bytes(data, 8)
        self.__keep_field1 = self.parse_bytes(data, 1)
        self.__capabilities_flags = Utils.byteOrderTransfer(self.parse_bytes(data, 2), 2)
        self.__character_set = self.parse_int(data, 1)
        self.__status_flags = self.parse_bytes(data, 2)
        self.__capabilities_flags = Utils.byteOrderTransfer(self.parse_bytes(data, 2), 2) + self.__capabilities_flags
        self.__capabilities_flags = int(self.__capabilities_flags, 16)
        if self.__capabilities_flags & Constants.CLIENT_PLUGIN_AUTH :
            self.__auth_plugin_data_len = self.parse_int(data, 1)
        self.__keep_field2 = self.parse_bytes(data, 10)
        if self.__capabilities_flags & Constants.CLIENT_SECURE_CONNECTION:
            length = max(13, self.__auth_plugin_data_len - 8)
            self.__auth_plugin_data = self.__auth_plugin_data + self.parse_bytes(data, length)
        self.__auth_plugin_data = a2b_hex(self.__auth_plugin_data[:-2])
        if self.__capabilities_flags & Constants.CLIENT_PLUGIN_AUTH:
            self.__auth_plugin_name = self.parse_string_by_split(data, '\x00')

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value


class ClientHandShakeMessage:
    def __init__(self):
        self.__capability_flags = Constants.CLIENT_PROTOCOL_41 \
                                  | Constants.CLIENT_PLUGIN_AUTH \
                                  | Constants.CLIENT_SECURE_CONNECTION \
                                  | Constants.CLIENT_CONNECT_WITH_DB
        self.__max_packet_size = 0      # 4 bytes
        self.__character_set = 0        # 1 byte
        self.__reserved = Utils.int2hex(0, 23)      # 23 bytes
        self.__user_name = ''           # NULL end
        self.__auth_response_length = 0 # 1 byte
        self.__auth_response = ''       # auth_response_length bytes
        self.__database = ''            # NULL end
        self.__auth_plugin_name = ''    # NULL end

    def set_character_set(self, set):
        self.__character_set = set

    def set_user_name(self, user_name):
        self.__user_name = user_name
        user_name_length = len(user_name)
        if user_name[user_name_length - 1] != '\0':
            self.__user_name += '\0'

    def set_auth_response(self, response):
        self.__auth_response = a2b_hex(response)
        self.__auth_response_length = len(self.__auth_response)

    def set_database(self, database):
        self.__database = database
        length = len(database)
        if database[length - 1] != '\0':
            self.__database += '\0'

    def set_auth_plugin_name(self, name):
        self.__auth_plugin_name = name
        name_length = len(name)
        if name[name_length - 1] != '\0':
            self.__auth_plugin_name += '\0'

    def package(self):
        buffer = ''
        buffer_length = 0

        buffer += a2b_hex(Utils.int2hex(self.__capability_flags, 4))
        buffer_length += 4

        buffer += a2b_hex(Utils.int2hex(self.max_size(), 4))
        buffer_length += 4

        buffer += a2b_hex(Utils.int2hex(self.__character_set, 1))
        buffer_length += 1

        buffer += a2b_hex(self.__reserved)
        buffer_length += 23


        buffer += self.__user_name
        buffer_length += len(self.__user_name)

        buffer += a2b_hex(Utils.int2hex(self.__auth_response_length, 1))
        buffer_length += 1

        buffer += self.__auth_response
        buffer_length += self.__auth_response_length

        buffer += self.__database
        buffer_length += len(self.__database)

        buffer += self.__auth_plugin_name
        buffer_length += len(self.__auth_plugin_name)

        return (buffer, buffer_length)

    def max_size(self):
        max_size = 4 + 1 + 23 \
                   + len(self.__user_name) \
                   + len(self.__auth_response) \
                   + len(self.__database) \
                   + len(self.__auth_plugin_name)

        return max_size

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

class ResponseMessage:
    def __init__(self):
        self.__header = 0x00
        self.__packet = None

    def parse(self, data):
        offset = 0
        self.__header = Utils.str2int(data, RESPONSE_PACKET_HEADER_BYTES)
        offset += RESPONSE_PACKET_HEADER_BYTES

        if self.__header == 0x00:
            self.__packet = ResponseMessageOK()
        elif self.__header == 0xFE:
            self.__packet = ResponseMessageEOF()
        elif self.__header == 0xFF:
            self.__packet = ResponseMessageERR()
        else:
            return False

        return self.__packet.parse(data[offset : ])

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value
        if self.__packet != None:
            self.__packet.dump()

class ResponseMessageOK(ResponseMessage):
    def __init__(self):
        self.__header = 0x00            # 1 byte
        self.__affected_rows = 0        # lenenc bytes
        self.__last_insert_id = 0       # lenenc bytes
        self.__status_flags = 0         # 2 bytes
        self.__warnings = 0             # 2 bytes
        self.__info = ''                 # lenenc bytes

    def parse(self, data):
        offset = 0
        (self.__affected_rows, passed) = Utils.str2lenencint(data[offset : ])
        offset += passed
        (self.__last_insert_id, passed) = Utils.str2lenencint(data[offset : ])
        offset += passed
        self.__status_flags = Utils.str2int(data[offset : ], RESPONSE_PACKET_STATUSFLAGS_BYTES)
        offset += RESPONSE_PACKET_STATUSFLAGS_BYTES
        self.__warnings = Utils.str2int(data[offset : ], RESPONSE_PACKET_WARNING_BYTES)
        offset += RESPONSE_PACKET_WARNING_BYTES
        self.__info = data[offset : ]

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

class ResponseMessageEOF(ResponseMessage):
    def __init__(self):
        self.__header = 0xFE        # 1 byte(defaule:0xfe)
        self.__warnings = 0         # 2 bytes
        self.__status_flags = 0     # 2 bytes

    def parse(self, data):
        offset = 0
        self.__warnings = Utils.str2int(data[offset : ], RESPONSE_PACKET_WARNING_BYTES)
        offset += RESPONSE_PACKET_WARNING_BYTES
        self.__status_flags = Utils.str2int(data[offset : ], RESPONSE_PACKET_STATUSFLAGS_BYTES)
        offset += RESPONSE_PACKET_STATUSFLAGS_BYTES
        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

class ResponseMessageERR(ResponseMessage):
    def __init__(self):
        self.__header = 0xFF        # 1 byte(defaule:0xfe)
        self.__error_code = 0       # 2 bytes
        self.__sql_state_marker = ''    # 1 byte
        self.__sql_state = ''       # 5 bytes
        self.__error_message = ''   # EOF

    def parse(self, data):
        offset = 0
        self.__error_code = Utils.str2int(data[offset : ], RESPONSE_PACKET_ERRORCODE_BYTES)
        offset += RESPONSE_PACKET_ERRORCODE_BYTES
        self.__sql_state_marker = data[offset : offset + RESPONSE_PACKET_SQLSTATEMARKER_BYTES]
        offset += RESPONSE_PACKET_SQLSTATEMARKER_BYTES
        self.__sql_state = data[offset : offset + RESPONSE_PACKET_SQLSTATE_BYTES]
        offset += RESPONSE_PACKET_SQLSTATE_BYTES
        self.__error_message = data[offset : ]
        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value