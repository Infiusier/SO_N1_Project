# coding: utf-8
from Enum import *

from Ponte import Bridge
from ManuseadorDeCarros import Bridge_Handler

if __name__=='__main__':
    
    direita = Direction.RIGHT
    esquerda = Direction.LEFT
    
    Bridge.new_bridge(direita)
    
    Bridge_Handler.new_handler(10)
    bridge_handler = Bridge_Handler.bridge_handler()
    
    #bridge_handler.append_car_to_bridge(5.0, 9.0, direita)
    #bridge_handler.append_car_to_bridge(7.0, 12.0, direita)
    #bridge_handler.append_car_to_bridge(3.0, 20.0, esquerda)
    #bridge_handler.append_car_to_bridge(9.0, 6.0, esquerda)
    #bridge_handler.append_car_to_bridge(5.0, 9.0, direita)
    #bridge_handler.append_car_to_bridge(7.0, 12.0, direita)
    #bridge_handler.append_car_to_bridge(3.0, 20.0, esquerda)
    #bridge_handler.append_car_to_bridge(9.0, 6.0, esquerda)
    bridge_handler.append_car_to_bridge(2, 1, direita)
    bridge_handler.append_car_to_bridge(0, 5, direita)
    
    bridge_handler.begin_bridge()
    
