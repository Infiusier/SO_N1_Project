# coding: utf-8
import threading,time
from Enum import *
from Bridge import Bridge

import Bridge_Handler
import pygame
#from Bridge_Handler import *

class Car(threading.Thread):
    def __init__(self,Id,waiting_time,crossing_time,car_direction,state=State.PARKED):
        super(Car,self).__init__()
        
        self.Id = Id
        self.waiting_time = waiting_time        #Tempo de espera
        self.crossing_time = crossing_time  #tempo de travessia
        self.state = state                  #State do carro
        self.car_direction = car_direction      #Direção do carro
        
        self.waited_time=0
        self.time_crossing=0
        self.crossing_percentage=0.0
        
        self.flip_car=0
        
        if self.car_direction==Direction.RIGHT:
            self.car_image_file=str(self.Id)+".png"
            self.carX=BRIDGE_RIGHT_OFFSET
            self.carY=380
            
        else:
            self.car_image_file=str(self.Id)+"f.png"
            self.carX=BRIDGE_LEFT_OFFSET
            self.carY=380
            
        self.car_image=pygame.image.load(self.car_image_file)
        
    
    def print_car(self):
        #print("Id: " + str(self.Id) + "State: " + str(self.state) + "Direction: " + str(self.car_direction))
        pass
        
    def run(self):
        
        self.now_time=0.0
        self.before_time=time.time()
        
        self.waited_time=0.0
        self.time_crossing=0.0

        print(str(self.Id)+" "+ str(time.time()))
        while(True):
            if(self.state == State.PARKED):                         
                self.parked_state()
                
            elif(self.state == State.WAITING):
                self.waiting_state()
            
            elif(self.state == State.CROSSING):
                self.crossing_state()  
    
    def test_collision(self):
        
        for car in Bridge_Handler.Bridge_Handler.bridge_handler().list_of_cars:
            
            if car.state==State.CROSSING:
                distance_crossed_1=int(980*(self.time_crossing/self.crossing_time))
                distance_crossed_2=int(980*(car.time_crossing/car.crossing_time))
                
                if distance_crossed_2>distance_crossed_1:
                    
                    if not(distance_crossed_2-45>distance_crossed_1):
                        
                        return False
        return True    
            
    def move_car(self):
        
        if self.car_direction==Direction.LEFT:
            print(self.carX)
            self.carX=BRIDGE_LEFT_OFFSET+int((BRIDGE_RIGHT_OFFSET-BRIDGE_LEFT_OFFSET)*(self.time_crossing/self.crossing_time))
            
        else:
            self.carX=BRIDGE_RIGHT_OFFSET-int((BRIDGE_RIGHT_OFFSET-BRIDGE_LEFT_OFFSET)*(self.time_crossing/self.crossing_time))
     
    def crossing_state(self):
    
        if self.test_collision():
            self.move_car()
            self.now_time = time.time()
            self.time_crossing += self.now_time - self.before_time
            self.before_time = self.now_time
        else:
            self.before_time = time.time()
            
            
        if(self.time_crossing >= self.crossing_time):    #trocar isso
            self.flip_car=1
            #print(str(self.Id)+" "+ str(time.time()))
            self.print_car()
            Bridge.mutex.acquire()
            Bridge.car_semaphore.acquire()
            if(Bridge.car_semaphore._value == 0):
                if (Bridge.number_of_cars == 0):   #Significa que não tem fila 
                    Bridge.bridge().bridge_direction=Direction.NONE
                    Bridge.bridge_semaphore.release()  #Libera a bridge pro proximo que chegar
                    Bridge.number_of_cars=0
                
                else:  #Significa que tem fila
                    #Bridge.bridge().bridge_direction=Direction.NONE
                    Bridge.bridge().bridge_direction=Bridge.bridge().bridge_priority
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
            self.print_car()
            self.state = State.WAITING
            self.waited_time = 0.0
    
    
    def flip_car_direction(self):
        if(self.car_direction == Direction.RIGHT):
            self.car_direction = Direction.LEFT
        
        else:
            self.car_direction = Direction.RIGHT