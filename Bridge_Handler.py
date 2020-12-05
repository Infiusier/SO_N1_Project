from Enum import *

from Car import Car

class Bridge_Handler():
    __object=None
    def __init__(self):
        self.list_of_cars=[]
    
    @staticmethod
    def new_handler():
        if(Bridge_Handler.__object==None):
            Bridge_Handler.__object =  Bridge_Handler()
        
    @staticmethod
    def bridge_handler():
        return Bridge_Handler.__object
    
    def get_car_new_id(self):
        car_ids=[]
        if len(self.list_of_cars)>0:
            for car in self.list_of_cars:
                car_ids.append(car.Id)
            new_ids=list(set(range(0, max(car_ids))).difference(car_ids))
            if len(new_ids)>0:
                return new_ids[0]
            else:
                return len(self.list_of_cars)
            
        else:  
            return 0    
    
    def append_car_to_bridge(self, waiting_time, crossing_time,car_direction,state=State.PARKED):
        self.list_of_cars.append(Car(Id=self.get_car_new_id(),waiting_time=waiting_time,crossing_time=crossing_time,state=state,car_direction=car_direction))


    def begin_bridge(self):
        for car in self.list_of_cars:
            car.start()