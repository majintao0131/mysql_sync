#!/usr/bin/env python
__author__ = 'jintao'

import threading

class BinlogHandler:
    def __init__(self, name):
        self.__handler_name = name

    def handler_name(self):
        return self.__handler_name

    def process(self, item):
        item.dump()

class BinlogHandlerManage:
    def __init__(self, binlogDataManage):
        self.__pipeline = []
        self.__binlogDataManage = binlogDataManage
        self.__count = 0

    def reset(self):
        self.__pipeline = []
        self.__count = 0

    def pipeline(self):
        return self.__pipeline

    def handler_count(self):
        return self.__count

    def add_last_handler(self, handler):
        self.__pipeline.append(handler)
        self.__count += 1

    def add_first_handler(self, handler):
        self.__pipeline.insert(0, handler)
        self.__count += 1

    def process(self, item):
        for handler in self.__pipeline:
            handler.process()

class HandlerThread(threading.Thread):
    def __init__(self, signal, binlogDataManage):
        threading.Thread.__init__(self)
        self.__signal = signal
        self.__binlogDataManage = binlogDataManage
        self.__binlogHandlerManage = BinlogHandlerManage(binlogDataManage)
        self.__exit = False

    def exit(self):
        self.__exit = True

    def run(self):
        while self.__exit == False:
            item = self.__binlogDataManage.pop()
            self.__signal.clear()
            if item == None:
                print 'wait...'
                self.__signal.wait()
                continue
            print 'process...'
            self.__binlogHandlerManage.process(item)
