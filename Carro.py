# coding: utf-8
import threading,time
from Enum import *
from Ponte import Bridge

import ManuseadorDeCarros

class Carro(threading.Thread):
    def __init__(self,Id,waiting_time,crossing_time,car_direction,state=State.PARKED):
        super(Carro,self).__init__()
        
        self.Id = Id
        self.waiting_time = waiting_time        #Tempo de espera
        self.crossing_time = crossing_time  #tempo de travessia
        self.state = state                  #State do carro
        self.car_direction = car_direction      #Direção do carro
        
        self.waited_time=0
        self.time_crossing=0
    
    def print_car(self):
        print("Id: " + str(self.Id) + "State: " + str(self.state) + "Direction: " + str(self.car_direction))
        
    def run(self):
        
        self.now_time=0.0
        self.before_time=time.time()
        
        self.waited_time=0.0
        self.time_crossing=0.0

        try:
            print(str(self.Id)+" "+ str(time.time()))
            while(True):
                
                if(self.state == State.PARKED):                         
                    self.parked_state()
                    
                
                elif(self.state == State.WAITING):
                    self.waiting_state()
                
                elif(self.state == State.CROSSING):
                    self.crossing_state()
                    
        except:
            print("deu ruim")
            
    def limit_car_speed(self):
        pass
     
    def crossing_state(self):
        
        self.now_time = time.time()
        self.time_crossing += self.now_time - self.before_time
        self.before_time = self.now_time
        if(self.time_crossing >= self.crossing_time):    #trocar isso
            print(str(self.Id)+" "+ str(time.time()))
            #Log.doLog(ManuseadorDeCarros.manuseador().getCarros())
            self.print_car()
            Bridge.mutex.acquire()
            Bridge.car_semaphore.acquire()
            if(Bridge.car_semaphore._value == 0):
                if (Bridge.number_of_cars == 0):   #Significa que não tem fila 
                    Bridge.bridge().bridge_direction=Direction.NONE
                    Bridge.bridge_semaphore.release()  #Libera a bridge pro proximo que chegar
                    Bridge.number_of_cars=0
                
                else:  #Significa que tem fila
                    Bridge.bridge().bridge_direction=Direction.NONE
                    for i in range(Bridge.number_of_cars):
                        Bridge.bridge_semaphore.release() #Libera todos os carros que estão na fila
                    Bridge.number_of_cars=0
                
            Bridge.mutex.release()
            self.flip_car_direction()#muda direcoa do carro
            self.state = State.PARKED#muda estado
            self.waited_time = 0.0
            self.now_time = 0.0
            self.before_time = time.time()  
            
            
    def waiting_state(self):
        
        Bridge.mutex.acquire()
        #Log.doLog(ManuseadorDeCarros.manuseador().getCarros())
        self.print_car()
        if((Bridge.bridge().bridge_direction == Direction.NONE) or (self.car_direction != Bridge.bridge().bridge_direction)):
            if (self.car_direction != Bridge.bridge().bridge_direction and Bridge.bridge().bridge_direction != Direction.NONE):
                Bridge.number_of_cars+=1
            
            Bridge.mutex.release()
            Bridge.bridge_semaphore.acquire()
            Bridge.mutex.acquire()
            Bridge.bridge().bridge_direction=self.car_direction
        
        Bridge.car_semaphore.release()
        Bridge.mutex.release()
        self.state = State.CROSSING    #se passou muda estado para atravessando
        self.time_crossing = 0.0 
        self.now_time = 0.0
        self.before_time = time.time()
            
            
    def parked_state(self):
        
        self.now_time = time.time()
        self.waited_time += self.now_time - self.before_time
        self.before_time = self.now_time
        if(self.waited_time >= self.waiting_time):
            #Log.doLog(ManuseadorDeCarros.manuseador().getCarros())
            self.print_car()
            self.state = State.WAITING
            self.waited_time = 0.0
    
    
    def flip_car_direction(self):
        if(self.car_direction == Direction.RIGHT):
            self.car_direction = Direction.LEFT
        
        else:
            self.car_direction = Direction.RIGHT