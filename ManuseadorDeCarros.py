from Enum import *

from Carro import Carro

class Bridge_Handler():
    __object=None
    def __init__(self,max_cars=0):
        
        self.max_cars=max_cars
        self.list_of_cars=[]
    
    @staticmethod
    def new_handler(max_cars):
        if(Bridge_Handler.__object==None):
            Bridge_Handler.__object =  Bridge_Handler(max_cars)
        
    @staticmethod
    def bridge_handler():
        return Bridge_Handler.__object
    
    def append_car_to_bridge(self, waiting_time, crossing_time,car_direction,state=State.PARKED,):
        self.list_of_cars.append(Carro(Id=len(self.list_of_cars),waiting_time=waiting_time,crossing_time=crossing_time,state=state,car_direction=car_direction))

    def begin_bridge(self):
        for car in self.list_of_cars:
            car.start()