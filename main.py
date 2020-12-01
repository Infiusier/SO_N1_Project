# coding: utf-8
from Enum import *

from Bridge import Bridge
from Bridge_Handler import Bridge_Handler
from screen import *
import threading,time,sys

if __name__=='__main__':
    
    pygame.init()
    pygame.display.set_caption("Problema da Ponte Estreita")
    icon = pygame.image.load('iconbridge.png')
    pygame.display.set_icon(icon)
    
    screen=Screen()
    
    direita = Direction.RIGHT
    esquerda = Direction.LEFT
    
    Bridge.new_bridge(direita)
    
    Bridge_Handler.new_handler(10)
    bridge_handler = Bridge_Handler.bridge_handler()
    
    bridge_handler.append_car_to_bridge(5, 9, esquerda)
    bridge_handler.append_car_to_bridge(7, 12, esquerda)
    bridge_handler.append_car_to_bridge(3, 20, esquerda)
    bridge_handler.append_car_to_bridge(9, 6, esquerda)
    bridge_handler.append_car_to_bridge(1, 35, esquerda)
    bridge_handler.append_car_to_bridge(6, 35, esquerda)
    bridge_handler.append_car_to_bridge(7, 35, esquerda)
    bridge_handler.append_car_to_bridge(26, 35, esquerda)
    bridge_handler.append_car_to_bridge(20, 35, direita)
    bridge_handler.append_car_to_bridge(25, 35, esquerda)
    
    bridge_handler.begin_bridge()
    

    while screen.running==True:
        start_time = time.time()
        
        screen.update()
        #mouse = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                screen.running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                screen.verify_input_clicked(event)
                    
                if screen.btn_criar_carro.collidepoint(event.pos):
                    screen.create_car()
                        
                if screen.btn_deletar_carro.collidepoint(event.pos):
                    screen.delete_car()
                        
                if screen.btn_ponte.collidepoint(event.pos):
                    screen.set_bridge_priority()
                        
            if event.type == pygame.KEYDOWN:
                screen.get_keyboard_input(event)
                            
        if screen.active_travessia:
            colort = screen.color_inputA
        
        else:
            colort= screen.color_inputB
            
        if screen.active_espera:
            colore= screen.color_inputA
            
        else:
            colore= screen.color_inputB
            
        if screen.active_direcao:
            colord= screen.color_inputA
            
        else:
            colord= screen.color_inputB
            
        if screen.active_deletar:
            colordel= screen.color_inputA
            
        else:
            colordel= screen.color_inputB
            
        if screen.active_ponte:
            colorpon= screen.color_inputA
            
        else:
            colorpon= screen.color_inputB
            
        pygame.draw.rect(screen.screen, colort, screen.txt_box_travessia,2)
        pygame.draw.rect(screen.screen, colore, screen.txt_box_espera,2)
        pygame.draw.rect(screen.screen, colord, screen.txt_box_direcao,2)
        pygame.draw.rect(screen.screen, colordel, screen.txt_box_deletar,2)
        pygame.draw.rect(screen.screen, colorpon, screen.txt_box_ponte,2)
        pygame.draw.rect(screen.screen, screen.color_buttons, screen.btn_criar_carro)
        pygame.draw.rect(screen.screen, screen.color_buttons, screen.btn_deletar_carro)
        pygame.draw.rect(screen.screen, screen.color_buttons, screen.btn_ponte)
    
        text_direcao_ponte = screen.base_font.render(screen.txt_direcao_ponte, True, (255,255,255))
        text_travessia = screen.base_font.render(screen.txt_tempo_travessia, True, (255,255,255))
        text_espera = screen.base_font.render(screen.txt_tempo_espera, True, (255,255,255))
        text_direcao = screen.base_font.render(screen.txt_direcao, True, (255,255,255))
        text_travessia_in = screen.base_font.render(screen.txt_input_travessia, True, (255,255,255))
        text_espera_in = screen.base_font.render(screen.txt_input_espera, True, (255,255,255))
        text_direcao_in = screen.base_font.render(screen.txt_input_direcao, True, (255,255,255))
        text_deletar_in = screen.base_font.render(screen.txt_input_deletar, True, (255,255,255))
        text_ponte_in = screen.base_font.render(screen.txt_input_ponte, True, (255,255,255))
        text_ponte = screen.base_font.render(screen.txt_ponte,True,(255,255,255))
        text_criar = screen.base_font.render(screen.txt_criar_carro, True, (255,255,255))
        text_definir = screen.base_font.render(screen.txt_btn_ponte, True, (255,255,255))  
        text_deletar = screen.base_font.render(screen.txt_deletar_carro, True, (255,255,255))
        text_instr_d = screen.font_instr.render(screen.txt_instruction_del, True, (255,255,255))
        text_instr_d2 = screen.font_instr.render(screen.txt_instruction_del2, True, (255,255,255))
        text_instr_di = screen.font_instr.render(screen.txt_instruction_dir, True, (255,255,255))
        text_instr_po = screen.font_instr.render(screen.txt_instruction_dir, True, (255,255,255))
        text_instr_tr = screen.font_instr.render(screen.txt_instruction_travessia, True, (255,255,255))
        text_instr_es = screen.font_instr.render(screen.txt_instruction_espera, True, (255,255,255))
        erro = screen.base_font.render(screen.txt_erro, True, (255,255,255))
        
        screen.screen.blit(text_travessia,(screen.txt_box_travessia.x-200,screen.txt_box_travessia.y+8))
        screen.screen.blit(text_espera,(screen.txt_box_espera.x-200,screen.txt_box_espera.y+8))
        screen.screen.blit(text_direcao,(screen.txt_box_direcao.x-200,screen.txt_box_direcao.y+8))
        screen.screen.blit(text_travessia_in, (screen.txt_box_travessia.x+5,screen.txt_box_travessia.y+8))
        screen.screen.blit(text_espera_in, (screen.txt_box_espera.x+5,screen.txt_box_espera.y+8))
        screen.screen.blit(text_direcao_in, (screen.txt_box_direcao.x+5,screen.txt_box_direcao.y+8))   
        screen.screen.blit(text_criar, (screen.btn_criar_carro.x+12,screen.btn_criar_carro.y+8))
        screen.screen.blit(text_deletar_in, (screen.txt_box_deletar.x+5,screen.txt_box_deletar.y+8))
        screen.screen.blit(text_deletar, (screen.btn_deletar_carro.x+5,screen.btn_deletar_carro.y+8)) #botãozinho
        screen.screen.blit(text_deletar, (screen.txt_box_deletar.x-0,screen.txt_box_deletar.y-65))
        screen.screen.blit(text_instr_d, (screen.txt_box_deletar.x-0,screen.txt_box_deletar.y-40))
        screen.screen.blit(text_instr_d2, (screen.txt_box_deletar.x-0,screen.txt_box_deletar.y-25))
        screen.screen.blit(text_instr_di, (screen.txt_box_direcao.x-200,screen.txt_box_direcao.y+25))
        screen.screen.blit(text_ponte_in, (screen.txt_box_ponte.x+5,screen.txt_box_ponte.y+8))
        screen.screen.blit(text_ponte, (screen.txt_box_ponte.x,screen.txt_box_ponte.y-65))
        screen.screen.blit(text_instr_po, (screen.txt_box_ponte.x,screen.txt_box_ponte.y-30))
        screen.screen.blit(text_instr_tr, (screen.txt_box_travessia.x-200,screen.txt_box_travessia.y+26))
        screen.screen.blit(text_instr_es, (screen.txt_box_espera.x-200,screen.txt_box_espera.y+26))
        screen.screen.blit(text_definir, (screen.btn_ponte.x+32 ,screen.btn_ponte.y+8))
        screen.screen.blit(erro, (400,650))
        screen.screen.blit(text_direcao_ponte, (450,100))
        
        screen.txt_box_direcao.w = max(90,text_direcao_in.get_width() + 10)
        screen.txt_box_ponte.w = max(90,text_ponte_in.get_width() + 10)
        
        pygame.display.update()
        
                
        try:
            #print("FPS: ", 1.0 / (time.time() - start_time))
            pass
        except:
            pass
        
        
    pygame.quit()
    sys.exit()
