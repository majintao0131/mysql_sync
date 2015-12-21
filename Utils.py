#!/usr/bin/env python

__author__ = 'jintao'

from binascii import hexlify
from hashlib import sha1
from binascii import a2b_hex, b2a_hex
import struct

class Utils:
    @staticmethod
    def hex2int(data, byte_count):
        buf = ''
        for i in range(0, byte_count):
            buf += data[i * 2 : (i + 1) * 2]

        return int(buf, 16)

    @staticmethod
    def int2hex(value, byte_count):
        buf = ''
        for i in range(0, byte_count):
            tmp = hex(value % 256)
            if len(tmp) < 4:
                buf += '0'
            buf += hex(value % 256)[2:]
            value /= 256

        return buf

    @staticmethod
    def byteOrderTransfer(data, byte_count):
        buf = ''
        for i in range(0, byte_count):
            buf += data[(byte_count - i - 1) * 2 : (byte_count - i) * 2]

        return buf

    @staticmethod
    def str2int(data, byte_count):
        if byte_count <= 0:
            return 0
        elif byte_count == 1:
            return int(b2a_hex(data[0]), 16)
        else:
            return Utils.hex2int(Utils.byteOrderTransfer(b2a_hex(data[0 : byte_count]), byte_count), byte_count)

    @staticmethod
    def str2int_bigendian(data, byte_count):
        if byte_count <= 0:
            return 0
        elif byte_count == 1:
            return int(b2a_hex(data[0]), 16)
        else:
            return Utils.hex2int(data[0, byte_count], byte_count)

    @staticmethod
    def str2double(data, byte_count):
        return struct.unpack("!f", Utils.byteOrderTransfer(b2a_hex(data[0 : byte_count]), byte_count).decode('hex'))[0]

    @staticmethod
    def str2float(data, byte_count):
        return struct.unpack("!f", Utils.byteOrderTransfer(b2a_hex(data[0 : byte_count]), byte_count).decode('hex'))[0]

    @staticmethod
    def str2lenencint(data):
        type = Utils.str2int(data, 1)
        if type < 0xFB:
            return (type, 1)
        elif type == 0xFC:
            return (Utils.str2int(data[1:], 2), 3)
        elif type == 0xFD:
            return (Utils.str2int(data[1:], 3), 4)
        elif type == 0xFE:
            return (Utils.str2int(data[1:], 8), 9)
        else:
            return (0, 0)

    @staticmethod
    def lenencint2str(value):
        return ''

    @staticmethod
    def secureAuthMethod(password, random_number):
        sha1_password = a2b_hex(sha1(password).hexdigest())
        sha1_sha1_pw = a2b_hex(sha1(sha1_password).hexdigest())
        sha1_random = a2b_hex(sha1(random_number + sha1_sha1_pw).hexdigest())

        length = len(sha1_random)
        result = ''
        for i in range(0, length):
            result += chr(ord(sha1_password[i]) ^ ord(sha1_random[i]))
        return b2a_hex(result)

    @staticmethod
    def bit2list(value, bit_count):
        bit_list = []
        bitmask = 1
        for i in range(bit_count):
            if value & bitmask != 0:
                bit_list.append(1)
            else:
                bit_list.append(0)

            bitmask *= 2
        return bit_list

    @staticmethod
    def bitlist1count(list):
        count = 0
        for i in list:
            if i == 1:
                count += 1
        return count

    @staticmethod
    def bitCount(value):
        count = 0
        while value != 0:
            count += 1
            value &= (value - 1)

        return count

    @staticmethod
    def mask(count):
        mask = 0
        bit = 1
        for i in range(count):
            mask |= bit
            bit *= 2

        return mask

