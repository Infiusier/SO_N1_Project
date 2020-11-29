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
        self.in_line_state=False
        
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
        
    def run(self):
        
        self.now_time=0.0
        self.before_time=time.time()
        
        self.waited_time=0.0
        self.time_crossing=0.0

        while(True):
            if(self.state == State.PARKED):                         
                self.parked_state()
                
            elif(self.state == State.WAITING):
                self.waiting_state()
                
            elif self.state==State.IN_LINE:
                self.in_line()
                
            elif(self.state == State.CROSSING):
                self.crossing_state()
    
    def verify_priority(self):
        if Bridge.bridge().bridge_priority != Priority.NONE:
            if self.car_direction!=Bridge.bridge().bridge_priority:
                Bridge.bridge_priority_semaphore.acquire()
                Bridge.bridge_priority_semaphore.release()
                
            else:
                if Bridge.bridge_priority_semaphore._value==1:
                    Bridge.bridge_priority_semaphore.acquire()
            
    def free_bridge_from_priority(self):
        if Bridge.bridge().bridge_priority != Priority.NONE:
            if self.car_direction==Bridge.bridge().bridge_priority:
                if Bridge.bridge().bridge_priority == Priority.RIGHT:
                    for i in range(len(Bridge.cars_l)):
                        print("release l")
                        Bridge.bridge_priority_semaphore.release()
                        
                else:
                    for i in range(len(Bridge.cars_r)):
                        print("release r")
                        Bridge.bridge_priority_semaphore.release()
            
                
    def in_line(self):
        self.before_time = time.time()
        if self.car_direction==Direction.LEFT:
            if Bridge.cars_l[0] == self.Id:
                self.state=State.CROSSING
        else:
            if Bridge.cars_r[0] == self.Id:
                self.state=State.CROSSING
                
    def free_next_car(self):
        if self.in_line_state==True:
            if ((self.carX > (BRIDGE_LEFT_OFFSET+45) and self.car_direction==Direction.LEFT) 
            or (self.carX < (BRIDGE_RIGHT_OFFSET-45) and self.car_direction==Direction.RIGHT)):
                self.in_line_state=False
                #print(Bridge.cars_list)
                if self.car_direction==Direction.LEFT:
                    Bridge.cars_l.pop(0)
                else:
                    Bridge.cars_r.pop(0)
                
    
    def test_collision(self):
        
        for car in Bridge_Handler.Bridge_Handler.bridge_handler().list_of_cars:
            
            if car.state==State.CROSSING:
                distance_crossed_1=int((BRIDGE_RIGHT_OFFSET-BRIDGE_LEFT_OFFSET)*(self.time_crossing/self.crossing_time))
                distance_crossed_2=int((BRIDGE_RIGHT_OFFSET-BRIDGE_LEFT_OFFSET)*(car.time_crossing/car.crossing_time))
                
                if distance_crossed_2>distance_crossed_1:
                    
                    if not(distance_crossed_2-45>distance_crossed_1):
                        
                        return False
        return True    
            
    def move_car(self):
        if self.car_direction==Direction.LEFT:
            self.carX=BRIDGE_LEFT_OFFSET+int((BRIDGE_RIGHT_OFFSET-BRIDGE_LEFT_OFFSET)*(self.time_crossing/self.crossing_time))
            
        else:
            self.carX=BRIDGE_RIGHT_OFFSET-int((BRIDGE_RIGHT_OFFSET-BRIDGE_LEFT_OFFSET)*(self.time_crossing/self.crossing_time))
     
    def crossing_state(self):
        
        if self.test_collision():
            self.free_next_car()
            self.move_car()
            self.now_time = time.time()
            self.time_crossing += self.now_time - self.before_time
            self.before_time = self.now_time
        else:
            self.before_time = time.time()
            
        if(self.time_crossing >= self.crossing_time):    #trocar isso
            self.flip_car=1
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
            self.free_bridge_from_priority()
            self.flip_car_direction()
            self.state = State.PARKED
            self.waited_time = 0
            self.now_time = 0
            self.before_time = time.time()  
            
            
    def waiting_state(self):
        self.append_car()
        self.verify_priority()
        Bridge.mutex.acquire()
        if((Bridge.bridge().bridge_direction == Direction.NONE) or (self.car_direction != Bridge.bridge().bridge_direction)):
            if (self.car_direction != Bridge.bridge().bridge_direction and Bridge.bridge().bridge_direction != Direction.NONE):
                Bridge.number_of_cars+=1
            
            Bridge.mutex.release()
            Bridge.bridge_semaphore.acquire()
            Bridge.mutex.acquire()
            Bridge.bridge().bridge_direction=self.car_direction
    
        Bridge.car_semaphore.release()
        Bridge.mutex.release()
        self.in_line_state=True
        self.state = State.IN_LINE
        self.time_crossing = 0
        self.now_time = 0
        self.before_time = time.time()
        
            
            
    def parked_state(self):
        
        self.now_time = time.time()
        self.waited_time += self.now_time - self.before_time
        self.before_time = self.now_time
        if(self.waited_time >= self.waiting_time):
            self.state = State.WAITING
            self.waited_time = 0
    
    def append_car(self):
        if self.car_direction==Direction.LEFT:  
            Bridge.cars_l.append(self.Id)
        else:
            Bridge.cars_r.append(self.Id)
    
    def flip_car_direction(self):
        if(self.car_direction == Direction.RIGHT):
            self.car_direction = Direction.LEFT
        
        else:
            self.car_direction = Direction.RIGHT