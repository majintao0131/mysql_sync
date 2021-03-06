#!/usr/bin/env python
__author__ = 'jintao'

"""
capability flags
"""

# Use the improved version of Old Password Authentication
CLIENT_LONG_PASSWORD = 0x00000001
# Send found rows instead of affected rows in EOF_Packet
CLIENT_FOUND_ROWS = 0x00000002
# Longer flags in Protocol::ColumnDefinition320
CLIENT_LONG_FLAG = 0x00000004
# Database (schema) name can be specified on connect in Handshake Response Packet
CLIENT_CONNECT_WITH_DB = 0x00000008
#
CLIENT_NO_SCHEMA = 0x00000010
# Compression protocol supported
CLIENT_COMPRESS = 0x00000020
# Special handling of ODBC behavior.
CLIENT_ODBC = 0x00000040
# Can use LOAD DATA LOCAL
CLIENT_LOCAL_FILES = 0x00000080
# Parser can ignore spaces before '('
CLIENT_IGNORE_SPACE = 0x00000100
# Supports the 4.1 protocol
CLIENT_PROTOCOL_41 = 0x00000200
# wait_timeout versus wait_interactive_timeout
CLIENT_INTERACTIVE = 0x00000400
# Supports SSL
CLIENT_SSL= 0x00000800
# Do not issue SIGPIPE if network failures occur
CLIENT_IGNORE_SIGPIPE = 0x00001000
# Can send status flags in EOF_Packet
CLIENT_TRANSACTIONS = 0x00002000
# Unused
CLIENT_RESERVED = 0x00004000
# Supports Authentication::Native41
CLIENT_SECURE_CONNECTION = 0x00008000
# Can handle multiple statements per COM_QUERY and COM_STMT_PREPARE
CLIENT_MULTI_STATEMENTS = 0x00010000
# Can send multiple resultsets for COM_QUERY
CLIENT_MULTI_RESULTS = 0x00020000
# Can send multiple resultsets for COM_STMT_EXECUTE
CLIENT_PS_MULTI_RESULTS = 0x00040000
# Sends extra data in Initial Handshake Packet and supports the pluggable authentication protocol
CLIENT_PLUGIN_AUTH = 0x00080000
# Permits connection attributes in Protocol::HandshakeResponse41
CLIENT_CONNECT_ATTRS = 0x00100000
# Understands length-encoded integer for auth response data in Protocol::HandshakeResponse41
CLIENT_PLUGIN_AUTH_LENENC_CLIENT_DATA = 0x00200000
# Announces support for expired password extension
CLIENT_CAN_HANDLE_EXPIRED_PASSWORDS = 0x00400000
# Can set SERVER_SESSION_STATE_CHANGED in the Status Flags and send session-state change data after a OK packet
CLIENT_SESSION_TRACK = 0x00800000
# Can send OK after a Text Resultset
CLIENT_DEPRECATE_EOF = 0x01000000


"""
command type
"""

COM_SLEEP = 0x00
COM_QUIT = 0x01
COM_INIT_DB = 0x02
COM_QUERY = 0x03
COM_FIELD_LIST = 0x04
COM_CREATE_DB = 0x05
COM_DROP_DB = 0x06
COM_REFRESH = 0x07
COM_SHUTDOWN = 0x08
COM_STATISTICS = 0x09
COM_PROCESS_INFO = 0x0A
COM_CONNECT = 0x0B
COM_PROCESS_KILL = 0x0C
COM_DEBUG = 0x0D
COM_PING = 0x0E
COM_TIME = 0x0F
COM_DELAYED_INSERT = 0x10
COM_CHANGE_USER = 0x11
COM_BINLOG_DUMP = 0x12
COM_TABLE_DUMP = 0x13
COM_CONNECT_OUT = 0x14
COM_REGISTER_SLAVE = 0x15
COM_STMT_PREPARE = 0x16
COM_STMT_EXECUTE = 0x17
COM_STMT_SEND_LONG_DATA = 0x18
COM_STMT_CLOSE = 0x19
COM_STMT_RESET = 0x1A
COM_SET_OPTION = 0x1B
COM_STMT_FETCH = 0x1C
COM_DAEMON = 0x1D
COM_BINLOG_DUMP_GTID = 0x1E
COM_RESET_CONNECTION = 0x1F

"""
server status
"""
SERVER_STATUS_IN_TRANS = 0x0001	            #a transaction is active
SERVER_STATUS_AUTOCOMMIT = 0x0002           # auto-commit is enabled
SERVER_MORE_RESULTS_EXISTS = 0x0008
SERVER_STATUS_NO_GOOD_INDEX_USED = 0x0010
SERVER_STATUS_NO_INDEX_USED = 0x0020
SERVER_STATUS_CURSOR_EXISTS = 0x0040        # Used by Binary Protocol Resultset to signal that COM_STMT_FETCH must be used to fetch the row-data.
SERVER_STATUS_LAST_ROW_SENT = 0x0080
SERVER_STATUS_DB_DROPPED = 0x0100
SERVER_STATUS_NO_BACKSLASH_ESCAPES = 0x0200
SERVER_STATUS_METADATA_CHANGED = 0x0400
SERVER_QUERY_WAS_SLOW = 0x0800
SERVER_PS_OUT_PARAMS = 0x1000
SERVER_STATUS_IN_TRANS_READONLY = 0x2000    # in a read-only transaction
SERVER_SESSION_STATE_CHANGED = 0x4000       # connection state information has changed

"""
Server Response Header
"""
SERVER_RESPONSE_OK = 0x00
SERVER_RESPONSE_EOF = 0xFE
SERVER_RESPONSE_ERR = 0xFF

"""
COMMAND FLAGS
"""
BINLOG_DUMP_NON_BLOCK = 0x01


"""
Binlog Event
"""
BINLOG_EVENT_HEADER = 19


"""
Binlog Event Type
"""
BINLOG_UNKNOWN_EVENT = 0x00
BINLOG_START_EVENT_V3 = 0x01
BINLOG_QUERY_EVENT = 0x02
BINLOG_STOP_EVENT = 0x03
BINLOG_ROTATE_EVENT = 0x04
BINLOG_INTVAR_EVENT = 0x05
BINLOG_LOAD_EVENT = 0x06
BINLOG_SLAVE_EVENT = 0x07
BINLOG_CREATE_FILE_EVENT = 0x08
BINLOG_APPEND_BLOCK_EVENT = 0x09
BINLOG_EXEC_LOAD_EVENT = 0x0a
BINLOG_DELETE_FILE_EVENT = 0x0b
BINLOG_NEW_LOAD_EVENT = 0x0c
BINLOG_RAND_EVENT = 0x0d
BINLOG_USER_VAR_EVENT = 0x0e
BINLOG_FORMAT_DESCRIPTION_EVENT = 0x0f
BINLOG_XID_EVENT = 0x10
BINLOG_BEGIN_LOAD_QUERY_EVENT = 0x11
BINLOG_EXECUTE_LOAD_QUERY_EVENT = 0x12
BINLOG_TABLE_MAP_EVENT = 0x13
BINLOG_WRITE_ROWS_EVENTv0 = 0x14
BINLOG_UPDATE_ROWS_EVENTv0 = 0x15
BINLOG_DELETE_ROWS_EVENTv0 = 0x16
BINLOG_WRITE_ROWS_EVENTv1 = 0x17
BINLOG_UPDATE_ROWS_EVENTv1 = 0x18
BINLOG_DELETE_ROWS_EVENTv1 = 0x19
BINLOG_INCIDENT_EVENT = 0x1a
BINLOG_HEARTBEAT_EVENT = 0x1b
BINLOG_IGNORABLE_EVENT = 0x1c
BINLOG_ROWS_QUERY_EVENT = 0x1d
BINLOG_WRITE_ROWS_EVENTv2 = 0x1e
BINLOG_UPDATE_ROWS_EVENTv2 = 0x1f
BINLOG_DELETE_ROWS_EVENTv2 = 0x20
BINLOG_GTID_EVENT = 0x21
BINLOG_ANONYMOUS_GTID_EVENT = 0x22
BINLOG_PREVIOUS_GTIDS_EVENT = 0x23

"""
Binlog Event Flag
"""
LOG_EVENT_BINLOG_IN_USE_F = 0x0001
LOG_EVENT_FORCED_ROTATE_F = 0x0002
LOG_EVENT_THREAD_SPECIFIC_F = 0x0004
LOG_EVENT_SUPPRESS_USE_F = 0x0008
LOG_EVENT_UPDATE_TABLE_MAP_VERSION_F = 0x0010
LOG_EVENT_ARTIFICIAL_F = 0x0020
LOG_EVENT_RELAY_LOG_F = 0x0040
LOG_EVENT_IGNORABLE_F = 0x0080
LOG_EVENT_NO_FILTER_F = 0x0100
LOG_EVENT_MTS_ISOLATE_F = 0x0200

"""
Intvar event type
"""
INTVAR_INVALID_INT_EVENT = 0x00
INTVAR_LAST_INSERT_ID_EVENT = 0x01
INTVAR_INSERT_ID_EVENT = 0x02

"""
Column Types
"""
MYSQL_TYPE_DECIMAL = 0x00       # Implemented by ProtocolBinary::MYSQL_TYPE_DECIMAL
MYSQL_TYPE_TINY = 0x01          # Implemented by ProtocolBinary::MYSQL_TYPE_TINY
MYSQL_TYPE_SHORT =  0x02        # Implemented by ProtocolBinary::MYSQL_TYPE_SHORT
MYSQL_TYPE_LONG = 0x03          # Implemented by ProtocolBinary::MYSQL_TYPE_LONG
MYSQL_TYPE_FLOAT = 0x04         # Implemented by ProtocolBinary::MYSQL_TYPE_FLOAT
MYSQL_TYPE_DOUBLE = 0x05        # Implemented by ProtocolBinary::MYSQL_TYPE_DOUBLE
MYSQL_TYPE_NULL = 0x06          # Implemented by ProtocolBinary::MYSQL_TYPE_NULL
MYSQL_TYPE_TIMESTAMP = 0x07     # Implemented by ProtocolBinary::MYSQL_TYPE_TIMESTAMP
MYSQL_TYPE_LONGLONG = 0x08      # Implemented by ProtocolBinary::MYSQL_TYPE_LONGLONG
MYSQL_TYPE_INT24 = 0x09         # Implemented by ProtocolBinary::MYSQL_TYPE_INT24
MYSQL_TYPE_DATE = 0x0a          # Implemented by ProtocolBinary::MYSQL_TYPE_DATE
MYSQL_TYPE_TIME = 0x0b          # Implemented by ProtocolBinary::MYSQL_TYPE_TIME
MYSQL_TYPE_DATETIME = 0x0c      # Implemented by ProtocolBinary::MYSQL_TYPE_DATETIME
MYSQL_TYPE_YEAR = 0x0d          # Implemented by ProtocolBinary::MYSQL_TYPE_YEAR
MYSQL_TYPE_NEWDATE = 0x0e       # see Protocol::MYSQL_TYPE_DATE
MYSQL_TYPE_VARCHAR = 0x0f       # Implemented by ProtocolBinary::MYSQL_TYPE_VARCHAR
MYSQL_TYPE_BIT = 0x10           # Implemented by ProtocolBinary::MYSQL_TYPE_BIT
MYSQL_TYPE_TIMESTAMP2 = 0x11    # see Protocol::MYSQL_TYPE_TIMESTAMP
MYSQL_TYPE_DATETIME2 = 0x12     # see Protocol::MYSQL_TYPE_DATETIME
MYSQL_TYPE_TIME2 = 0x13         # see Protocol::MYSQL_TYPE_TIME
MYSQL_TYPE_NEWDECIMAL= 0xf6     # Implemented by ProtocolBinary::MYSQL_TYPE_NEWDECIMAL
MYSQL_TYPE_ENUM = 0xf7          # Implemented by ProtocolBinary::MYSQL_TYPE_ENUM
MYSQL_TYPE_SET = 0xf8           # Implemented by ProtocolBinary::MYSQL_TYPE_SET
MYSQL_TYPE_TINY_BLOB = 0xf9     # Implemented by ProtocolBinary::MYSQL_TYPE_TINY_BLOB
MYSQL_TYPE_MEDIUM_BLOB = 0xfa   # Implemented by ProtocolBinary::MYSQL_TYPE_MEDIUM_BLOB
MYSQL_TYPE_LONG_BLOB = 0xfb     # Implemented by ProtocolBinary::MYSQL_TYPE_LONG_BLOB
MYSQL_TYPE_BLOB = 0xfc          # Implemented by ProtocolBinary::MYSQL_TYPE_BLOB
MYSQL_TYPE_VAR_STRING = 0xfd    # Implemented by ProtocolBinary::MYSQL_TYPE_VAR_STRING
MYSQL_TYPE_STRING = 0xfe        # Implemented by ProtocolBinary::MYSQL_TYPE_STRING
MYSQL_TYPE_GEOMETRY = 0xff


"""
Query Event Status Vars
"""
Q_FLAGS2_CODE = 0x00
Q_SQL_MODE_CODE = 0x01
Q_CATALOG = 0x02
Q_AUTO_INCREMENT = 0x03
Q_CHARSET_CODE = 0x04
Q_TIME_ZONE_CODE = 0x05
Q_CATALOG_NZ_CODE = 0x06
Q_LC_TIME_NAMES_CODE = 0x07
Q_CHARSET_DATABASE_CODE = 0x08
Q_TABLE_MAP_FOR_UPDATE_CODE = 0x09
Q_MASTER_DATA_WRITTEN_CODE = 0x0a
Q_INVOKERS = 0x0b
Q_UPDATED_DB_NAMES = 0x0c
Q_MICROSECONDS = 0x0d


"""
MySQL Operation Type
"""
MySQL_COMMAND_INSERT = 0x01
MySQL_COMMAND_UPDATE = 0x02
MYSQL_COMMAND_DELETE = 0x03