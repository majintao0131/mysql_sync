#!/usr/bin/env python
__author__ = 'jintao'

from binascii import b2a_hex, a2b_hex
from binascii import hexlify
from Utils import Utils

PACKET_PAYLOAD_LENGTH_BYTES = 3
PACKET_INDEX_BYTES = 1

class PacketManage:
    def __init__(self):
        self.__list = []
        self.__list_count = 0

    def packet_list(self):
        return self.__list

    def parse(self, data):
        left_data_count = len(data)
        while left_data_count > 0 and len(data) > 0:
            packet = Packet()
            (data, pass_count) = packet.parse(data)
            self.__list.append(packet)
            self.__list_count += 1
            left_data_count -= pass_count

        return (self.__list, self.__list_count)

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

