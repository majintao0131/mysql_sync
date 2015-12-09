#!/usr/bin/env python
__author__ = 'jintao'

from binascii import b2a_hex, a2b_hex
from binascii import hexlify
from Utils import Utils
from BinlogEvent import BinlogEventManage
from BinlogDataManage import BinlogDataManage, BinlogData
from Message import ResponseMessage
import Constants

PACKET_PAYLOAD_LENGTH_BYTES = 3
PACKET_INDEX_BYTES = 1

class PacketManage:
    def __init__(self, binlog_event_manage, binlog_data_manage):
        self.__list = []
        self.__event_list = []
        self.__list_count = 0
        self.__binlog_event_manage = binlog_event_manage
        self.__binlog_data_manage = binlog_data_manage

    def packet_list(self):
        return self.__list

    def parse(self, data):
        left_data_count = len(data)
        index = 0
        while left_data_count > 0 and len(data) > 0:
            packet = Packet()
            (data, pass_count) = packet.parse(data)

            # print '-------- packet ' + str(packet.index()) + '-----------'
            packet_type = Utils.str2int(packet.payload(), 1)
            if packet_type == 0x00:
                binlog_event = self.__binlog_event_manage.append(packet.payload())
                self.__parse2data(binlog_event)
                index += 1
            else:
                packet_eof = ResponseMessage()
                packet_eof.parse(packet.payload())
                packet_eof.dump()

            self.__list.append(packet)
            self.__list_count += 1
            left_data_count -= pass_count

        return (self.__list, self.__list_count)

    def __parse2data(self, binlog_event):
        if binlog_event == None:
            return True

        if binlog_event.header().event_type() == Constants.BINLOG_ROTATE_EVENT:
            self.__binlog_data_manage.set_filename(binlog_event.event_body().next_binlog())     # set binlog file name
        elif binlog_event.header().event_type() == Constants.BINLOG_WRITE_ROWS_EVENTv0 \
            or binlog_event.header().event_type() == Constants.BINLOG_WRITE_ROWS_EVENTv1 \
            or binlog_event.header().event_type() == Constants.BINLOG_WRITE_ROWS_EVENTv2 \
            or binlog_event.header().event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv0 \
            or binlog_event.header().event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv1 \
            or binlog_event.header().event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv2 \
            or binlog_event.header().event_type() == Constants.BINLOG_DELETE_ROWS_EVENTv0 \
            or binlog_event.header().event_type() == Constants.BINLOG_DELETE_ROWS_EVENTv1 \
            or binlog_event.header().event_type() == Constants.BINLOG_DELETE_ROWS_EVENTv2:
            command_type = Constants.MySQL_COMMAND_INSERT
            if binlog_event.header().event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv0 \
                or binlog_event.header().event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv1 \
                or binlog_event.header().event_type() == Constants.BINLOG_UPDATE_ROWS_EVENTv2:
                command_type = Constants.MySQL_COMMAND_UPDATE
            else:
                command_type = Constants.MYSQL_COMMAND_DELETE

            table_map_event = self.__binlog_event_manage.last_table_map_event()
            table_name = table_map_event.event_body().table_name()
            column_count = table_map_event.event_body().column_count()
            binlog_data = BinlogData(command_type, table_name, column_count)
            changed_rows = binlog_event.event_body().rows()
            for changed_row in changed_rows:
                binlog_data.append_columns(changed_row)

            if command_type == Constants.MySQL_COMMAND_UPDATE:
                for changed_row in changed_rows:
                    binlog_data.append_columns_update(changed_row)
                if binlog_data.rows_count() != binlog_data.rows_update_count():
                    return False
            self.__binlog_data_manage.push(binlog_data)

        elif binlog_event.header().event_type() == Constants.BINLOG_XID_EVENT:
            self.__binlog_data_manage.set_position(binlog_event.header().log_pos())
        else:
            pass

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

class Packet:
    def __init__(self):
        self.__payload_length = 0                                 # 3 bytes
        self.__index = 0                                          # 1 bytes
        self.__payload = None                                     # payload_length bytes

    def set_payload(self, payload, payload_length):
        self.__payload_length = payload_length
        self.__payload = payload

    def payload(self):
        return self.__payload

    def payload_length(self):
        return self.__payload_length

    def set_index(self, index):
        self.__index = index

    def index(self):
        return self.__index

    def parse(self, data):
        offset = 0
        global PACKET_INDEX_BYTES, PACKET_PAYLOAD_LENGTH_BYTES
        self.__payload_length = Utils.str2int(data[offset:], PACKET_PAYLOAD_LENGTH_BYTES)
        offset += PACKET_PAYLOAD_LENGTH_BYTES
        self.__index = Utils.str2int(data[offset:], PACKET_INDEX_BYTES)
        offset += PACKET_INDEX_BYTES
        self.__payload = data[offset : offset + self.__payload_length]
        offset += self.__payload_length
        if offset >= len(data):
            return ("", offset)

        return (data[offset:], offset)

    def package(self):
        bytes = a2b_hex(Utils.int2hex(self.__payload_length, PACKET_PAYLOAD_LENGTH_BYTES))

        hex_index = hex(self.__index)[2:]
        if len(hex_index) < (PACKET_PAYLOAD_LENGTH_BYTES + PACKET_INDEX_BYTES):
            hex_index = '0' + hex_index
        bytes += a2b_hex(hex_index)
        bytes += self.__payload

        return (bytes, self.__payload_length + PACKET_PAYLOAD_LENGTH_BYTES + PACKET_INDEX_BYTES)

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

