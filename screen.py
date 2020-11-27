import pygame
import threading
import time

from Car import *
from Bridge_Handler import *

class Screen(threading.Thread):
    def __init__(self):
        super(Screen,self).__init__()
        self.background = pygame.image.load('bridge.png')
        self.running = True
        self.screen = pygame.display.set_mode((1079,650))
    
    
    def park_in_left_side(self,car):
        if car.Id==0:
            car.carX=12
            car.carY=380
            
        elif car.Id==1:
            car.carX=12
            car.carY=380-50
            
        elif car.Id==2:
            car.carX=12
            car.carY=380-100
            
        elif car.Id==3:
            car.carX=12+80
            car.carY=380-300
            
        elif car.Id==4:
            car.carX=12+80
            car.carY=380-350
            
        elif car.Id==5:
            car.carX=12
            car.carY=380-250
            
        elif car.Id==6:
            car.carX=12
            car.carY=380-300
            
        elif car.Id==7:
            car.carX=12
            car.carY=380-350
            
        elif car.Id==8:
            car.carX=12+80
            car.carY=380
            
        elif car.Id==9:
            car.carX=12+80
            car.carY=380-50
        
    def park_in_right_side(self,car):
        if car.Id==0:
            car.carX=12+980
            car.carY=380
            
        elif car.Id==1:
            car.carX=12+980
            car.carY=380-50
            
        elif car.Id==2:
            car.carX=12+980
            car.carY=380-100
            
        elif car.Id==3:
            car.carX=12+980-80
            car.carY=380-300
            
        elif car.Id==4:
            car.carX=12+980-80
            car.carY=380-250
            
        elif car.Id==5:
            car.carX=12+980
            car.carY=380-250
            
        elif car.Id==6:
            car.carX=12+980
            car.carY=380-300
            
        elif car.Id==7:
            car.carX=12+980
            car.carY=380-350
            
        elif car.Id==8:
            car.carX=12-80+980
            car.carY=380
            
        elif car.Id==9:
            car.carX=12-80+980
            car.carY=380-50
    
    def flip_car_image(self,car):
        if "f" in car.car_image_file:
            car.car_image_file=str(car.Id)+".png"
            
        else:
            car.car_image_file=str(car.Id)+"f.png"
            print(car.car_image_file)
            
        car.car_image=pygame.image.load(car.car_image_file)
        car.flip_car=0
        
    def update(self):
        
        self.screen.blit(self.background,(0,0))
        
        for car in Bridge_Handler.bridge_handler().list_of_cars:
            
            if car.flip_car==1:
                self.flip_car_image(car)
                
            if car.state==State.CROSSING:
            
                if car.carX<=12:
                    car.carX = 12
                    car.carY = 380
                    
                if car.carX>=980:
                    car.carX = 980
                    car.carY = 380        
            
            if car.state==State.PARKED:
                #car.carY=380
                
                if car.carX>500:
                    self.park_in_right_side(car)
                
                else:
                    self.park_in_left_side(car)
                    
            elif car.state==State.CROSSING:
                car.carY=200
                
            self.screen.blit(car.car_image,(car.carX,car.carY))
                
            