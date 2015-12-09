#!/usr/bin/env python

__author__ = 'jintao'

import thread

def singleton(cls, *args, **kw):
    instances = {}
    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

@singleton
class BinlogDataManage:
    def __init__(self):
        self.__lock = thread.allocate_lock()
        self.__list = []
        self.__list_count = 0
        self.__position = 0
        self.__filename = ''

    def push(self, binlog_data):
        self.__lock.acquire()
        self.__list.append(binlog_data)
        self.__list_count += 1
        self.__lock.release()

    def pop(self):
        self.__lock.acquire()
        if self.__list_count == 0:
            item = None
        else:
            item = self.__list.pop()
            self.__list_count -= 1
        self.__lock.release()

        return item

    def count(self):
        return self.__list_count

    def set_position(self, pos):
        self.__position = pos

    def position(self):
        return self.__position

    def set_filename(self, filename):
        self.__filename = filename

    def filename(self):
        return self.__filename

class BinlogData:
    def __init__(self, type, table, column_count):
        self.__type = type
        self.__table = table
        self.__columns_count = column_count
        self.__rows_count = 0
        self.__rows_update_count = 0
        self.__columns = []
        self.__columns_update = []

    def type(self):
        return self.__type

    def columns_count(self):
        return self.__columns_count

    def columns(self):
        return self.__columns

    def columns_update(self):
        return self.__columns_update

    def rows_count(self):
        return self.__rows_count

    def rows_update_count(self):
        return  self.__rows_update_count

    def append_columns(self, row):
        self.__columns.append(row)
        self.__rows_count += 1

    def append_columns_update(self, row):
        self.__columns_update.append(row)
        self.__rows_update_count += 1

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value
