#!/usr/bin/env python

__author__ = 'jintao'

import Constants
from Utils import Utils
from binascii import a2b_hex

"""
Register Command
struct:
    command type : 1 byte
    server id : 4 bytes
    slaves hostname length : 1 byte
    slaves hostname : (slaves hostname length) bytes
    slaves user len : 1 byte
    slaves user : (slaves user len) bytes
    slaves password len : 1 byte
    slaves password : (slaves password len) bytes
    slaves mysql port : 2 bytes
    replication rank : 4 bytes
    master id : 4 bytes
"""
class CommandRegisterSlave:
    def __init__(self,
                 server_id,
                 slaves_hostname_length,
                 slaves_hostname,
                 slaves_user_len,
                 slaves_user,
                 slaves_password_len,
                 slaves_password,
                 slaves_mysql_port,
                 master_id,
                 replication_rank = 0):
        self.__com_type = Constants.COM_REGISTER_SLAVE
        self.__server_id = server_id
        self.__slaves_hostname_length = slaves_hostname_length
        self.__slaves_hostname = slaves_hostname
        self.__slaves_user_len = slaves_user_len
        self.__slaves_user = slaves_user
        self.__slaves_password_len = slaves_password_len
        self.__slaves_password = slaves_password
        self.__slaves_mysql_port = slaves_mysql_port
        self.__replication_rank = replication_rank
        self.__master_id = master_id

    def set_server_id(self, server_id):
        self.__server_id = server_id

    def set_slaves_hostname(self, hostname, length):
        self.__slaves_hostname = hostname
        self.__slaves_hostname_length = length

    def set_slaves_user(self, user_name, len):
        self.__slaves_user = user_name
        self.__slaves_user_len = len

    def set_slaves_password(self, password, len):
        self.__slaves_password = password
        self.__slaves_password_len = len

    def set_slaves_mysql_port(self, port):
        self.__slaves_mysql_port = port

    def set_replication_rank(self, rank):
        self.__replication_rank = rank

    def set_master_id(self, master_id):
        self.__master_id = master_id

    def package(self):
        buffer = ''
        buf_len = 0

        buffer += a2b_hex(Utils.int2hex(self.__com_type, 1))
        buf_len += 1

        buffer += a2b_hex(Utils.int2hex(self.__server_id, 4))
        buf_len += 4

        buffer += a2b_hex(Utils.int2hex(self.__slaves_hostname_length, 1))
        buf_len += 1

        buffer += self.__slaves_hostname
        buf_len += self.__slaves_hostname_length

        buffer += a2b_hex(Utils.int2hex(self.__slaves_user_len, 1))
        buf_len += 1

        buffer += self.__slaves_user
        buf_len += self.__slaves_user_len

        buffer += a2b_hex(Utils.int2hex(self.__slaves_password_len, 1))
        buf_len += 1

        buffer += self.__slaves_password
        buf_len += self.__slaves_password_len

        buffer += a2b_hex(Utils.int2hex(self.__slaves_mysql_port, 2))
        buf_len += 2

        buffer += a2b_hex(Utils.int2hex(self.__replication_rank, 4))
        buf_len += 4

        buffer += a2b_hex(Utils.int2hex(self.__master_id, 4))
        buf_len += 4

        return (buffer, buf_len)

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value

class CommandDumpBinlog:
    def __init__(self, binlog_pos, flags, server_id, binlog_filename):
        self.__com_type = Constants.COM_BINLOG_DUMP         # 1 byte
        self.__binlog_pos = binlog_pos                      # 4 bytes
        self.__flags = flags                                # 2 bytes
        self.__server_id = server_id                        # 4 bytes
        self.__binlog_filename = binlog_filename            # NULL end

    def set_binlog_pos(self, pos):
        self.__binlog_pos = pos

    def set_flags(self, flags):
        self.__flags |= flags

    def set_server_id(self, server_id):
        self.__server_id = server_id

    def set_binlog_filename(self, filename):
        self.__binlog_filename = filename

    def package(self):
        buffer = ''
        buf_len = 0

        buffer += a2b_hex(Utils.int2hex(self.__com_type, 1))
        buf_len += 1

        buffer += a2b_hex(Utils.int2hex(self.__binlog_pos, 4))
        buf_len += 4

        buffer += a2b_hex(Utils.int2hex(self.__flags, 2))
        buf_len += 2

        buffer += a2b_hex(Utils.int2hex(self.__server_id, 4))
        buf_len += 4

        buffer += self.__binlog_filename
        buf_len += len(self.__binlog_filename)

        return (buffer, buf_len)

class CommandQuitBinlog:
    def __init__(self):
        self.__com_type = Constants.COM_QUIT

    def package(self):
        buffer = ''
        buf_len = 0
        buffer += a2b_hex(Utils.int2hex(self.__com_type, 1))
        buf_len += 1

        return (buffer, buf_len)