# coding: utf-8

from Enum import *
import threading

class Bridge():
    __object = None
    bridge_priority_semaphore=threading.Semaphore(1)
    bridge_semaphore = threading.Semaphore(1)
    cars_l=[]
    cars_r=[]
    number_of_left=0
    number_of_right=0
    left_mutex=threading.Semaphore(1)
    right_mutex=threading.Semaphore(1)
    def __init__(self,priority):                                
        self.bridge_priority = priority                                    
        
    @staticmethod
    def new_bridge(priority):
        if(Bridge.__object == None):
            Bridge.__object = Bridge(priority);
        
    @staticmethod
    def bridge():
        return Bridge.__object;