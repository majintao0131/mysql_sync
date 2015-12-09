#!/usr/bin/env python

__author__ = 'jintao'

import ConfigParser
import string, os, sys

class ConfigLoader:
    def __init__(self):
        self.__host = ''
        self.__port = 3306
        self.__username = ''
        self.__password = ''
        self.__database = ''
        self.__pos = 0
        self.__binlog = ''

    def host(self):
        return self.__host

    def port(self):
        return self.__port

    def username(self):
        return self.__username

    def password(self):
        return  self.__password

    def database(self):
        return self.__database

    def pos(self):
        return self.__pos

    def binlog(self):
        return self.__binlog

    def load(self, config_file):
        try :
            config = ConfigParser.ConfigParser()
            config.read(config_file)
            secs = config.sections()

            self.__host = config.get('db', 'db_host')
            self.__port = config.getint('db', 'db_port')
            self.__username = config.get('db', 'db_user')
            self.__password = config.get('db', 'db_pass')
            self.__database = config.get('db', 'db_name')
            self.__pos = config.getint('db', 'db_pos')
            self.__binlog = config.get('db', 'db_binlog')
        except :
            return False

        return True

    def dump(self):
        for property, value in vars(self).iteritems():
            print property, ": ", value


