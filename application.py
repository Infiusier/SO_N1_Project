# coding: utf-8
from Enum import *
from Bridge import Bridge
from Bridge_Handler import Bridge_Handler
from screen import *
import sys
from PySide2.QtCore import QThread

class Application(QThread):
    
    def __init__(self):
        super(Application,self).__init__()
        pygame.init()
        pygame.display.set_caption("Problema da Ponte Estreita")
        icon = pygame.image.load('iconbridge.png')
        pygame.display.set_icon(icon)
        self.screen=Screen()
    
    def run(self):
        
        direita = Direction.RIGHT
        esquerda = Direction.LEFT
        
        Bridge.new_bridge(direita)
        
        Bridge_Handler.new_handler()
        bridge_handler = Bridge_Handler.bridge_handler()
        '''
        bridge_handler.append_car_to_bridge(1, 13, esquerda)
        bridge_handler.append_car_to_bridge(2, 12, esquerda)
        bridge_handler.append_car_to_bridge(3, 20, esquerda)
        bridge_handler.append_car_to_bridge(4, 6, esquerda)
        bridge_handler.append_car_to_bridge(5, 35, esquerda)
        bridge_handler.append_car_to_bridge(6, 35, esquerda)
        bridge_handler.append_car_to_bridge(7, 35, esquerda)
        bridge_handler.append_car_to_bridge(8, 35, esquerda)
        bridge_handler.append_car_to_bridge(9, 35, esquerda)
        bridge_handler.append_car_to_bridge(0, 15, esquerda)
        
        bridge_handler.begin_bridge()
        '''
    
        while self.screen.running==True:
            start_time = time.time()
            
            self.screen.update()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.screen.running = False
                    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.screen.verify_input_clicked(event)
                        
                    if self.screen.btn_criar_carro.collidepoint(event.pos):
                        self.screen.create_car()
                            
                    if self.screen.btn_deletar_carro.collidepoint(event.pos):
                        self.screen.delete_car()
                            
                    if self.screen.btn_ponte.collidepoint(event.pos):
                        self.screen.set_bridge_priority()
                            
                if event.type == pygame.KEYDOWN:
                    self.screen.get_keyboard_input(event)
                                
            if self.screen.active_travessia:
                colort = self.screen.color_inputA
            
            else:
                colort= self.screen.color_inputB
                
            if self.screen.active_espera:
                colore= self.screen.color_inputA
                
            else:
                colore= self.screen.color_inputB
                
            if self.screen.active_direcao:
                colord= self.screen.color_inputA
                
            else:
                colord= self.screen.color_inputB
                
            if self.screen.active_deletar:
                colordel= self.screen.color_inputA
                
            else:
                colordel= self.screen.color_inputB
                
            if self.screen.active_ponte:
                colorpon= self.screen.color_inputA
                
            else:
                colorpon= self.screen.color_inputB
                
            pygame.draw.rect(self.screen.screen, colort, self.screen.txt_box_travessia,2)
            pygame.draw.rect(self.screen.screen, colore, self.screen.txt_box_espera,2)
            pygame.draw.rect(self.screen.screen, colord, self.screen.txt_box_direcao,2)
            pygame.draw.rect(self.screen.screen, colordel, self.screen.txt_box_deletar,2)
            pygame.draw.rect(self.screen.screen, colorpon, self.screen.txt_box_ponte,2)
            pygame.draw.rect(self.screen.screen, self.screen.color_buttons, self.screen.btn_criar_carro)
            pygame.draw.rect(self.screen.screen, self.screen.color_buttons, self.screen.btn_deletar_carro)
            pygame.draw.rect(self.screen.screen, self.screen.color_buttons, self.screen.btn_ponte)
        
            text_direcao_ponte = self.screen.base_font.render(self.screen.txt_direcao_ponte, True, (255,255,255))
            text_travessia = self.screen.base_font.render(self.screen.txt_tempo_travessia, True, (255,255,255))
            text_espera = self.screen.base_font.render(self.screen.txt_tempo_espera, True, (255,255,255))
            text_direcao = self.screen.base_font.render(self.screen.txt_direcao, True, (255,255,255))
            text_travessia_in = self.screen.base_font.render(self.screen.txt_input_travessia, True, (255,255,255))
            text_espera_in = self.screen.base_font.render(self.screen.txt_input_espera, True, (255,255,255))
            text_direcao_in = self.screen.base_font.render(self.screen.txt_input_direcao, True, (255,255,255))
            text_deletar_in = self.screen.base_font.render(self.screen.txt_input_deletar, True, (255,255,255))
            text_ponte_in = self.screen.base_font.render(self.screen.txt_input_ponte, True, (255,255,255))
            text_ponte = self.screen.base_font.render(self.screen.txt_ponte,True,(255,255,255))
            text_criar = self.screen.base_font.render(self.screen.txt_criar_carro, True, (255,255,255))
            text_definir = self.screen.base_font.render(self.screen.txt_btn_ponte, True, (255,255,255))  
            text_deletar = self.screen.base_font.render(self.screen.txt_deletar_carro, True, (255,255,255))
            text_instr_d = self.screen.font_instr.render(self.screen.txt_instruction_del, True, (255,255,255))
            text_instr_d2 = self.screen.font_instr.render(self.screen.txt_instruction_del2, True, (255,255,255))
            text_instr_di = self.screen.font_instr.render(self.screen.txt_instruction_dir, True, (255,255,255))
            text_instr_po = self.screen.font_instr.render(self.screen.txt_instruction_dir, True, (255,255,255))
            text_instr_tr = self.screen.font_instr.render(self.screen.txt_instruction_travessia, True, (255,255,255))
            text_instr_es = self.screen.font_instr.render(self.screen.txt_instruction_espera, True, (255,255,255))
            erro = self.screen.base_font.render(self.screen.txt_erro, True, (255,255,255))
            
            self.screen.screen.blit(text_travessia,(self.screen.txt_box_travessia.x-200,self.screen.txt_box_travessia.y+8))
            self.screen.screen.blit(text_espera,(self.screen.txt_box_espera.x-200,self.screen.txt_box_espera.y+8))
            self.screen.screen.blit(text_direcao,(self.screen.txt_box_direcao.x-200,self.screen.txt_box_direcao.y+8))
            self.screen.screen.blit(text_travessia_in, (self.screen.txt_box_travessia.x+5,self.screen.txt_box_travessia.y+8))
            self.screen.screen.blit(text_espera_in, (self.screen.txt_box_espera.x+5,self.screen.txt_box_espera.y+8))
            self.screen.screen.blit(text_direcao_in, (self.screen.txt_box_direcao.x+5,self.screen.txt_box_direcao.y+8))   
            self.screen.screen.blit(text_criar, (self.screen.btn_criar_carro.x+12,self.screen.btn_criar_carro.y+8))
            self.screen.screen.blit(text_deletar_in, (self.screen.txt_box_deletar.x+5,self.screen.txt_box_deletar.y+8))
            self.screen.screen.blit(text_deletar, (self.screen.btn_deletar_carro.x+5,self.screen.btn_deletar_carro.y+8)) #bot�ozinho
            self.screen.screen.blit(text_deletar, (self.screen.txt_box_deletar.x-0,self.screen.txt_box_deletar.y-65))
            self.screen.screen.blit(text_instr_d, (self.screen.txt_box_deletar.x-0,self.screen.txt_box_deletar.y-40))
            self.screen.screen.blit(text_instr_d2, (self.screen.txt_box_deletar.x-0,self.screen.txt_box_deletar.y-25))
            self.screen.screen.blit(text_instr_di, (self.screen.txt_box_direcao.x-200,self.screen.txt_box_direcao.y+25))
            self.screen.screen.blit(text_ponte_in, (self.screen.txt_box_ponte.x+5,self.screen.txt_box_ponte.y+8))
            self.screen.screen.blit(text_ponte, (self.screen.txt_box_ponte.x,self.screen.txt_box_ponte.y-65))
            self.screen.screen.blit(text_instr_po, (self.screen.txt_box_ponte.x,self.screen.txt_box_ponte.y-30))
            self.screen.screen.blit(text_instr_tr, (self.screen.txt_box_travessia.x-200,self.screen.txt_box_travessia.y+26))
            self.screen.screen.blit(text_instr_es, (self.screen.txt_box_espera.x-200,self.screen.txt_box_espera.y+26))
            self.screen.screen.blit(text_definir, (self.screen.btn_ponte.x+32 ,self.screen.btn_ponte.y+8))
            self.screen.screen.blit(erro, (400,650))
            self.screen.screen.blit(text_direcao_ponte, (450,100))
            
            self.screen.txt_box_direcao.w = max(90,text_direcao_in.get_width() + 10)
            self.screen.txt_box_ponte.w = max(90,text_ponte_in.get_width() + 10)
            
            pygame.display.update()
            
            
            try:
                #print("FPS: ", 1.0 / (time.time() - start_time))
                #print(Bridge.left_mutex._value,Bridge.right_mutex._value,Bridge.bridge_semaphore._value,Bridge.number_of_left,Bridge.number_of_right)
                pass
            except:
                pass
            
            
        pygame.quit()
        sys.exit()
