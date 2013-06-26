#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import logging.handlers
import os

NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL
MAXLOGSIZE = 10*1024*1024 #Bytes
BACKUPCOUNT = 10


formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s\t Thread-%(thread)d - %(message)s")

def getLogger(module_name):
    logger = MyLogger(module_name)
    return logger

def FileHandler(log_name):
    file_handler = MyFileHandler(log_name)
    return file_handler

class MyLogger():
    def __init__(self, module_name):
        self.__logger = logging.getLogger(module_name)

    def addHandler(self, handler):
        self.__logger.addHandler(handler.getHandler())

    def setLevel(self, level):
        self.__logger.setLevel(level)

    def debug(self, content):
        #cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #log_info = "[%s] <Log Level: Debug>: %s"%(cur_time, content)
        log_info = content
        self.__logger.debug(log_info)
        
    def info(self, content):
        #cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #log_info = "[%s] <Log Level: Info>: %s"%(cur_time, content)
        log_info = content
        self.__logger.info(log_info)

    def warning(self, content):
        #cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #log_info = "[%s] <Log Level: Warning>: %s"%(cur_time, content)
        log_info = content
        self.__logger.warning(log_info)

    def error(self, content):
        #cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #log_info = "[%s] <Log Level: Error>: %s"%(cur_time, content)
        log_info = content
        self.__logger.error(log_info)

    def critical(self, content):
        #cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #log_info = "[%s] <Log Level: Critical>: %s"%(cur_time, content)
        log_info = content
        self.__logger.critical(log_info)

class MyFileHandler():
    def __init__(self, log_name):
        self.__handler = logging.FileHandler(filename = log_name)
        self.__handler.setFormatter(formatter) 
        
    def getHandler(self):
        return self.__handler

class MyRotatingFileHandler():
    def __init__(self, log_name):
        self.__handler = logging.handlers.RotatingFileHandler(filename = log_name, maxBytes = MAXLOGSIZE, backupCount = BACKUPCOUNT)
        self.__handler.setFormatter(formatter) 
        
    def getHandler(self):
        return self.__handler

class MyStreamHandler():
    def __init__(self):
        self.__handler = logging.StreamHandler()
        self.__handler.setFormatter(formatter) 
        
    def getHandler(self):
        return self.__handler

def InitLog (module_name, log_name = "default.log", log_level = DEBUG, log_path = "./log/"):
    #log_path = "/opt/nagios/var/log/"
    if os.path.exists(log_path) == False:
        os.mkdir(log_path)
    logger = getLogger(module_name)
    filehandler = MyRotatingFileHandler(log_path + log_name)
    streamhandler = MyStreamHandler()
    logger.addHandler(filehandler)
    logger.addHandler(streamhandler)
    logger.setLevel(log_level)
    return logger

if __name__ == "__main__":
    logger = InitLog(module_name = "test" )
    logger.debug("test")

