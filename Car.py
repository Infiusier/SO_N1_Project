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
        self.is_running=True
        
        
        self.car_status="Carro %d: --" % self.Id
        
        
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

        while(self.is_running==True):
            
            self.car_status="Carro %d: %s" % (self.Id,self.state)
            
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
                if Bridge.bridge_priority_semaphore._value==0:
                    Bridge.bridge_priority_semaphore.acquire()
                
                
            else:
                if Bridge.bridge_priority_semaphore._value==1:
                    Bridge.bridge_priority_semaphore.acquire()
            
    def free_bridge_from_priority(self):
        if Bridge.bridge().bridge_priority != Priority.NONE:
            if self.car_direction==Bridge.bridge().bridge_priority:
                if Bridge.bridge_priority_semaphore._value==0:
                    Bridge.bridge_priority_semaphore.release()
            
                
    def in_line(self):
        time.sleep(0.1)
        self.before_time = time.time()
        
        if self.car_direction==Direction.LEFT:
            if len(Bridge.cars_l) > 0:
                if Bridge.cars_l[0] == self.Id:
                    self.state=State.CROSSING
        else:
            if len(Bridge.cars_r)>0:
                if Bridge.cars_r[0] == self.Id:
                    self.state=State.CROSSING
                
    def free_next_car(self):
        if self.in_line_state==True:
            if ((self.carX > (BRIDGE_LEFT_OFFSET+60) and self.car_direction==Direction.LEFT) 
            or (self.carX < (BRIDGE_RIGHT_OFFSET-60) and self.car_direction==Direction.RIGHT)):
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
            self.move_car()
            self.free_next_car()
            self.now_time = time.time()
            time.sleep(0.01)
            self.time_crossing += self.now_time - self.before_time
            self.before_time = self.now_time
        else:
            time.sleep(0.3)
            self.before_time = time.time()
            
        if(self.time_crossing >= self.crossing_time):
            self.state = State.PARKED
            
            self.flip_car=1
            if self.car_direction==Direction.LEFT:
                Bridge.left_mutex.acquire()
                Bridge.number_of_left-=1
                
                if Bridge.number_of_left==0:
                    Bridge.bridge_semaphore.release()
                
                Bridge.left_mutex.release()
                    
            else:
                Bridge.right_mutex.acquire()
                Bridge.number_of_right-=1
                
                if Bridge.number_of_right==0:
                    Bridge.bridge_semaphore.release()
                    
                Bridge.right_mutex.release()
                
            self.free_bridge_from_priority()
            self.flip_car_direction()
            self.waited_time = 0
            self.now_time = 0
            self.before_time = time.time()
            #print(Bridge.left_mutex._value,Bridge.right_mutex._value,Bridge.bridge_semaphore._value,Bridge.number_of_left,Bridge.number_of_right)
            
            
    def waiting_state(self):
       
        self.append_car()
        self.verify_priority()
        if self.car_direction==Direction.LEFT:
            Bridge.left_mutex.acquire()
            
            if self.is_running==False:
                Bridge.left_mutex.release()
                return
        
            if Bridge.number_of_left==0:
                Bridge.bridge_semaphore.acquire()
            
            
                
            if self.is_running==False:
                if Bridge.number_of_right==0:
                    Bridge.bridge_semaphore.release()
                return
            
            self.state=State.IN_LINE
            
            Bridge.number_of_left+=1
            
            Bridge.left_mutex.release()
            
        else:
            Bridge.right_mutex.acquire()
            
            if self.is_running==False:
                Bridge.right_mutex.release()
                return
            
            if Bridge.number_of_right==0:
                Bridge.bridge_semaphore.acquire()
                
            if self.is_running==False:
                if Bridge.number_of_left==0:
                    Bridge.bridge_semaphore.release()
                return
            
            self.state=State.IN_LINE
            
            Bridge.number_of_right+=1
            
            Bridge.right_mutex.release()
        
        self.time_crossing = 0
        self.now_time = 0
        self.before_time = time.time()
        self.in_line_state=True
        
            
            
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