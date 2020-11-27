from Enum import *

from Car import Car

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
    
    def find_missing(self,lst): 
        return [x for x in range(lst[0], lst[-1]+1)if x not in lst] 
    
    def get_car_new_id(self):
        if len(self.list_of_cars)>0:
            id_list=[]
            for car in self.list_of_cars:
                id_list.append(car.Id)
            new_id=self.find_missing(id_list)
            if len(new_id)==0:
                return len(self.list_of_cars)
            
        else:
            minimum_id=0
            
        return minimum_id    
    
    def append_car_to_bridge(self, waiting_time, crossing_time,car_direction,state=State.PARKED):
        self.list_of_cars.append(Car(Id=self.get_car_new_id(),waiting_time=waiting_time,crossing_time=crossing_time,state=state,car_direction=car_direction))

    def begin_bridge(self):
        for car in self.list_of_cars:
            car.start()