# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:33:15 2022

@author: Алёша
"""

from threading import Thread, Lock
#from asyncio import Lock
import time

class halfduplex_channel():
    
    def thread_waiter(self):
        while 1:
            self.waiterlock.acquire()
            #print("start waiting")
            time.sleep(len(self.data) / self.speed + self.latency)
            #self.inlock.release()
            if self.outlock.locked(): self.outlock.release()
            
    def __init__(self, speed = 1, latency = 0):
        self.speed = speed
        self.latency = latency
        self.data = []
        self.inlock = Lock()
        
        self.outlock = Lock()
        self.outlock.acquire()
        
        self.waiterlock = Lock()
        self.waiterlock.acquire()
        
        self.waiterthread = Thread(target = self.thread_waiter)
        self.waiterthread.start()

    def input(self, data = []): 
        self.inlock.acquire()
        self.data = data
        #self.outlock.acquire()
        if self.waiterlock.locked(): self.waiterlock.release()
        #print("data in to the channel")
        #self.inlock.release()
            
    def output(self):
        self.outlock.acquire()
        outdata = self.data
        if self.inlock.locked():self.inlock.release()
        #self.outlock.release()
        #print("data out from the channel")
        return outdata
    
testchannel = halfduplex_channel(speed = 1000, latency = 0.1)

pcie = halfduplex_channel(speed = 100)
membusin = halfduplex_channel(speed = 1000)
membusout = halfduplex_channel(speed = 1000)

def gpu_array():
    membus.input([i for i in range(1000)])
    
def producer():
    for i in range(1000):
        testchannel.input([1, 2, 3, 4, 5, 6, 7, 8, 9, i])
def receptor():
    for i in range(1000):
        print(testchannel.output())
        


Thread(target = producer).start()
Thread(target = receptor).start()
    