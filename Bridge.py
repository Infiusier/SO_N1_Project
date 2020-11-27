# coding: utf-8

from Enum import *
import threading

class Bridge():
    __object = None
    bridge_semaphore = threading.Semaphore(1)              #Controla o acesso a bridge
    car_semaphore = threading.Semaphore(0)                    #Numero de carros na bridge
    mutex = threading.Semaphore(1)                    #Controle de regiões "criticas"
    number_of_cars = 0                                           #Guarda o numero de carros do outro lado da bridge +1
    def __init__(self,priority):
        
        self.bridge_direction = Direction.NONE                                    #Direção da bridge
        self.bridge_priority = priority                                     #Prioridade da bridge
        
    @staticmethod
    def new_bridge(priority):
        if(Bridge.__object == None):
            Bridge.__object = Bridge(priority);
        
    @staticmethod
    def bridge():
        return Bridge.__object;