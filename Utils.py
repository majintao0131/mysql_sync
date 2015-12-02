#!/usr/bin/env python

__author__ = 'jintao'

from binascii import hexlify
from hashlib import sha1
from binascii import a2b_hex, b2a_hex

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
    def decodeLenencInteger(data):
        return 0

    @staticmethod
    def encodeLenencInteger(value):
        return ''