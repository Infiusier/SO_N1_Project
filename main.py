# coding: utf-8
from Enum import *

from Bridge import Bridge
from Bridge_Handler import Bridge_Handler
from screen import *
import threading,time

if __name__=='__main__':
    
    pygame.init()
    pygame.display.set_caption("Problema da Bridge Estreita")
    icon = pygame.image.load('iconbridge.png')
    pygame.display.set_icon(icon)
    
    screen=Screen()
    
    direita = Direction.RIGHT
    esquerda = Direction.LEFT
    
    Bridge.new_bridge(direita)
    
    Bridge_Handler.new_handler(10)
    bridge_handler = Bridge_Handler.bridge_handler()
    
    #bridge_handler.append_car_to_bridge(5, 9, esquerda)
    #bridge_handler.append_car_to_bridge(7, 12, esquerda)
    #bridge_handler.append_car_to_bridge(3, 20, esquerda)
    #bridge_handler.append_car_to_bridge(9, 6, esquerda)
    #bridge_handler.append_car_to_bridge(5, 9, esquerda)
    #bridge_handler.append_car_to_bridge(7, 12, esquerda)
    #bridge_handler.append_car_to_bridge(3, 20, esquerda)
    #bridge_handler.append_car_to_bridge(5, 10, esquerda)
    bridge_handler.append_car_to_bridge(7, 9, esquerda)
    bridge_handler.append_car_to_bridge(9, 8, esquerda)
    
    bridge_handler.begin_bridge()
    

    while screen.running==True:
        start_time = time.time()
        screen.update()
        pygame.display.update()
        
        #Close when quit button is pressed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.running = False
            
                
            #Move Car
        try:
            print("FPS: ", 1.0 / (time.time() - start_time))
        except:
            pass
        
        
    pygame.quit()

    
    
    
    
   
    
 
   

    
    
    
    
    
