#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading

class Worker (threading.Thread):
    worker_count = 0
    def __init__(self):
        threading.Thread.__init__(self) #base class func
        self.id = Worker.worker_count
        Worker.worker_count += 1
        self.stop = False
        self.working = False
        self.setDaemon(True)
        self.callable = None
        self.args = None
        self.kwds = None
        self.run_event = threading.Event()
        self.start()

        
    # in the other way, use __call__()
    def run(self):
        ''' the get-some-work, do-some-work main loop of worker threads '''   
        while True:
            self.run_event.wait()
            if self.working == True:
                callable = self.callable
                args = self.args
                kwds = self.kwds
                res = callable(*args, **kwds)
                self.working = False
                self.run_event.clear()
            if self.stop == True and self.working == False:
                self.run_event.clear()
                break

    def add_job(self, callable, *args, **kwds):
        self.callable = callable
        self.args = args
        self.kwds = kwds
        self.working = True
        self.run_event.set()
        
    def stop_worker(self):
        self.stop = True
        self.run_event.set()
        
class Thread_Pool ():
    def __init__ (self, thread_count = 10, timeout = 10):
        self.threads = []
        self.__create_threads(thread_count)
        self.__lock = threading.Lock()
        self.__destroy = False
        self.timeout = timeout
    def __create_threads (self, thread_count):
        for i in range(thread_count):
            worker = Worker()
            self.threads.append(worker)

    def __wait_for_complete_ex(self):
        for worker in self.threads:
            worker.join(self.timeout)
            
    def __wait_for_complete( self):  
        # ...then, wait for each of them to terminate:
        while len(self.threads):
            thread = self.threads.pop()
            #等待线程结束
            if thread.isAlive():#判断线程是否还存活来决定是否调用join
                thread.join(self.timeout)


    def destroy(self):
        self.__lock.acquire()
        for worker in self.threads:
            worker.stop_worker()
        self.__wait_for_complete()
        self.__destroy = True
        self.__lock.release() 

    def add_job (self, callable, *args, **kwds):
        self.__lock.acquire()
        bRet = False
        if self.__destroy == False:
            for worker in self.threads:
                if worker.working == False:
                    worker.add_job(callable, *args, **kwds)
                    bRet = True
                    break
        self.__lock.release()
        return bRet
		
		
	


