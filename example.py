__author__ = 'jintao'

import socket
from binascii import b2a_hex, a2b_hex
from Packet import Packet, PacketManage
from Message import ServerHandShakeMessage, ClientHandShakeMessage, ResponseMessage
from Utils import Utils
from MySQLCommand import CommandRegisterSlave
from MySQLCommand import CommandDumpBinlog
import Constants
from MYSQLChannel import MYSQLChannel

hand_shake_buffer = '4e0000000a352e352e34362d6c6f67001c0000005f5d39417960566e00fff72102000f80150000000000000000000047575e556c434778483f4474006d7973716c5f6e61746976655f70617373776f726400'
hand_shake_response = '0700000200000002000000'
register_response = '0700000100000002000000'
query_service_id = '200000000353484f57205641524941424c4553204c494b4520275345525645525f494427'
def handShakeService():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('127.0.0.1', 3306)

    sock.bind(server_address)
    sock.listen(10)

    while True:
        connection, client_address = sock.accept()
        print connection, client_address
        connection.send(a2b_hex(hand_shake_buffer))

        data = connection.recv(512)
        print b2a_hex(data)

        connection.send(a2b_hex(hand_shake_response))
        data = connection.recv(512)
        print b2a_hex(data)

        connection.send(a2b_hex(register_response))
        data = connection.recv(512)
        print b2a_hex(data)

    sock.close()

def package_handshake_response(pk, request):
    res_pk = Packet()
    res_mg = ClientHandShakeMessage()

    res_mg.set_character_set(request.character_set())
    res_mg.set_user_name('mysql_sync\0')
    res_mg.set_auth_plugin_name('mysql_native_password\0')
    res_mg.set_database('advert_database\0')
    res_mg.set_auth_response(Utils.secureAuthMethod('123456', request.auth_plugin_data()))

    #res_mg.dump()
    (buffer, length) = res_mg.package()

    res_pk.set_index(pk.index() + 1)
    res_pk.set_payload(buffer, length)

    return res_pk.package()

def package_register():
    reg_package = Packet()
    com_reg = CommandRegisterSlave(100,
                                   len('127.0.0.1'),
                                   '127.0.0.1',
                                   len('mysql_sync'),
                                   'mysql_sync',
                                   len('123456'),
                                   '123456',
                                   3306,
                                   1)

    (pack, pack_len) = com_reg.package()

    reg_package.set_payload(pack, pack_len)
    reg_package.set_index(0)

    return reg_package.package()

def package_dump():
    dump_package = Packet()
    com_dump = CommandDumpBinlog(872, Constants.BINLOG_DUMP_NON_BLOCK, 100, "data.000009")

    (buffer, buf_len) = com_dump.package()

    dump_package.set_index(0)
    dump_package.set_payload(buffer, buf_len)

    return dump_package.package()




def naive_client():
    # client
    address = ('127.0.0.1', 3306)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)

    data = s.recv(512)
    print '========== hand shake ==========='
    print '++++++++++ server to client +++++++++++++'
    print repr(data)
    print b2a_hex(data)

    pk = Packet()
    mg = ServerHandShakeMessage()
    pk.parse(data)
    mg.parse(pk.payload_length(), pk.payload())

    (response_packet, pack_len) = package_handshake_response(pk, mg)
    print '++++++++++ client to server +++++++++++++'
    print repr(response_packet)
    print b2a_hex(response_packet)
    s.send(response_packet)
    data = s.recv(512)

    print repr(data)
    print b2a_hex(data)

    print '========== register ==========='
    (reg_packet, reg_pack_len) = package_register()
    print '++++++++++ client to server +++++++++++++'
    print repr(reg_packet)
    print b2a_hex(reg_packet)
    s.send(reg_packet)
    data = s.recv(1024)
    print '++++++++++ server to client +++++++++++++'
    print repr(data)

    print '========== query service id ==========='
    query_packet = a2b_hex(query_service_id)
    print '++++++++++ client to server +++++++++++++'
    print query_service_id
    s.send(query_packet)
    data = s.recv(1024)
    print '++++++++++ server to client +++++++++++++'
    print repr(data)
    print b2a_hex(data)

    print '========== dump ==========='
    (dump_packet, dump_pack_len) = package_dump()
    print '++++++++++ client to server +++++++++++++'
    print repr(dump_packet)
    print b2a_hex(dump_packet)
    s.send(dump_packet)

    print '++++++++++ server to client header +++++++++++++'
    data = s.recv(1024)
    read_data = data
    while len(data) == 1024:
        s.recv(1024)
        read_data += data

    print repr(read_data)
    print b2a_hex(read_data)

    packetManage = PacketManage()
    (packet_list, count) = packetManage.parse(read_data)

    print '++++++++++ server to client header +++++++++++++'

    s.close()

naive_client()
#handShakeService()
