#!/usr/bin/env python

__author__ = 'jintao'

import socket
from Message import ServerHandShakeMessage, ClientHandShakeMessage, ResponseMessage
from Packet import Packet, PacketManage
from Utils import Utils
import Constants
from MySQLCommand import CommandRegisterSlave, CommandDumpBinlog, CommandQuitBinlog
from binascii import b2a_hex, a2b_hex

class MYSQLChannel:
    def __init__(self, hostname, port, username, password, database, master_id = 1, slave_id = 1000):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.__hostname = hostname
        self.__port = port
        self.__username = username
        self.__database = database
        self.__password = password
        self.__master_id = master_id
        self.__slave_id = slave_id
        self.__data = ''

    def __create_handshake_response(self):
        server_pk = Packet()
        server_mg = ServerHandShakeMessage()
        server_pk.parse(self.__data)
        server_mg.parse(server_pk.payload_length(), server_pk.payload())

        res_pk = Packet()
        res_mg = ClientHandShakeMessage()

        res_mg.set_character_set(server_mg.character_set())
        res_mg.set_user_name(self.__username)
        res_mg.set_auth_plugin_name(server_mg.auth_plugin_name())
        res_mg.set_database(self.__database)
        res_mg.set_auth_response(Utils.secureAuthMethod(self.__password, server_mg.auth_plugin_data()))

        (buffer, length) = res_mg.package()

        res_pk.set_index(server_pk.index() + 1)
        res_pk.set_payload(buffer, length)

        return res_pk.package()

    def __response_result(self):
        server_pk = Packet()
        server_mg = ResponseMessage()
        server_pk.parse(self.__data)
        server_mg.parse(server_pk.payload())

        if server_mg.header() == Constants.SERVER_RESPONSE_OK:
            return True
        elif server_mg.header() == Constants.SERVER_RESPONSE_EOF:
            return True
        elif server_mg.header() == Constants.SERVER_RESPONSE_ERR:
            return False

    def __handShake(self):
        self.__sock.connect((self.__hostname, self.__port))
        while True:
            data = self.__sock.recv(1024)
            self.__data += data
            if len(data) < 1024:
                break

        (response_packet, pack_len) = self.__create_handshake_response()

        self.__sock.send(response_packet)
        self.__data = ''
        while True:
            data = self.__sock.recv(1024)
            self.__data += data
            if len(data) < 1024:
                break

        return self.__response_result()

    def __package_register(self):
        reg_package = Packet()
        com_reg = CommandRegisterSlave(self.__slave_id,
                                       len(self.__hostname),
                                       self.__hostname,
                                       len(self.__username),
                                       self.__username,
                                       len(self.__password),
                                       self.__password,
                                       self.__port,
                                       self.__master_id)

        reg_package.set_payload(com_reg.package()[0], com_reg.package()[1])
        reg_package.set_index(0)

        return reg_package.package()

    def __register(self):
        (register_packet, packet_len) = self.__package_register()
        self.__sock.send(register_packet)
        self.__data = ''
        while True:
            data = self.__sock.recv(1024)
            self.__data += data
            if len(data) < 1024:
                break

        return self.__response_result()

    def initChannel(self):
        if self.__handShake() == False:
            return False

        if self.__register() == False:
            return False

        return True

    def __package_dump(self, position, filename):
        dump_package = Packet()
        com_dump = CommandDumpBinlog(position, Constants.BINLOG_DUMP_NON_BLOCK, self.__slave_id, filename)

        (buffer, buf_len) = com_dump.package()

        dump_package.set_index(0)
        dump_package.set_payload(buffer, buf_len)

        return dump_package.package()

    def dump_binlog(self, position, filename):
        (dump_packet, dump_pack_len) = self.__package_dump(position, filename)
        self.__sock.send(dump_packet)

        self.__data = ''
        while True:
            data = self.__sock.recv(1024)
            self.__data += data
            if len(data) < 1024:
                break

        print b2a_hex(data)
        return data

    def __package_close(self):
        close_package = Packet()
        com_close = CommandQuitBinlog()
        (buffer, buf_len) = com_close.package()

        close_package.set_index(0)
        close_package.set_payload(buffer, buf_len)

        return close_package.package()

    def close(self):
        (close_package, close_pack_len) = self.__package_close()
        self.__sock.send(close_package)
        self.__data = ''

        return True

