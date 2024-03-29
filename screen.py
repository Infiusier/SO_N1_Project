# coding: utf-8
from Car import *
from Bridge_Handler import *

class Screen():
    
    def __init__(self):
        super(Screen,self).__init__()
        
        self.gui_controller=GUI_Controller()
        
        self.screen = pygame.display.set_mode((1406,670))
        self.background = pygame.image.load('bridge.png')
        self.running = True
        self.base_font = pygame.font.Font(None,26)
        self.font_instr = pygame.font.Font(None,18)
        self.txt_input_travessia = ''
        self.txt_input_espera = ''
        self.txt_input_direcao = ''
        self.txt_input_deletar = ''
        self.txt_input_ponte = ''
        self.txt_erro = ''
        self.txt_direcao_ponte = 'Direção da Ponte: <---'
        self.txt_instruction_travessia = 'Digite números a partir de 10'
        self.txt_instruction_espera = 'Digite números a partir de 0'
        self.txt_instruction_dir = 'Digite Leste-Oeste ou Oeste-Leste'
        self.txt_instruction_del = 'Digite o numero do carro que'
        self.txt_instruction_del2 = 'deseja deletar (0-9)'
        self.txt_criar_carro = 'Criar Carro'
        self.txt_deletar_carro = 'Deletar Carro'
        self.txt_tempo_travessia = 'Tempo de Travessia:'
        self.txt_tempo_espera = 'Tempo de Espera:'
        self.txt_direcao = 'Direção do Carro:'
        self.txt_ponte = 'Direção da Ponte'
        self.txt_btn_ponte = 'Definir'
        
        self.label_car0 = 'Carro 0:'
        self.label_car1 = 'Carro 1:'
        self.label_car2 = 'Carro 2:'
        self.label_car3 = 'Carro 3:'
        self.label_car4 = 'Carro 4:'
        self.label_car5 = 'Carro 5:'
        self.label_car6 = 'Carro 6:'
        self.label_car7 = 'Carro 7:'
        self.label_car8 = 'Carro 8:'
        self.label_car9 = 'Carro 9:'
        self.status_car0 = '--'
        self.status_car1 = '--'
        self.status_car2 = '--'
        self.status_car3 = '--'
        self.status_car4 = '--'
        self.status_car5 = '--'
        self.status_car6 = '--'
        self.status_car7 = '--'
        self.status_car8 = '--'
        self.status_car9 = '--'
        
        #Rectangles//buttons and boxes
        self.txt_box_travessia = pygame.Rect(965,480,90,32)
        self.txt_box_espera = pygame.Rect(965,520,90,32)
        self.txt_box_direcao = pygame.Rect(965,560,90,32)
        self.btn_criar_carro = pygame.Rect(910,610,120,30)
        self.txt_box_deletar = pygame.Rect(550,550,90,32)
        self.btn_deletar_carro = pygame.Rect(550,610,120,30)
        self.txt_box_ponte = pygame.Rect(320,550,90,32)
        self.btn_ponte = pygame.Rect(320,610,120,30)
        
        #Colors to textboxes and buttons
        self.color_inputA = pygame.Color(30,50,200)
        self.color_inputB = pygame.Color(200,200,200)
        self.color_buttons = (60,40,255)
        self.color = self.color_inputB#Possible unused
        
        self.active_travessia = False
        self.active_espera = False
        self.active_direcao = False
        self.active_deletar = False
        self.active_ponte = False
        
    def flip_car_image(self,car):
        if "f" in car.car_image_file:
            car.car_image_file=str(car.Id)+".png"
            
        else:
            car.car_image_file=str(car.Id)+"f.png"
            #print(car.car_image_file)
            
        car.car_image=pygame.image.load(car.car_image_file)
        car.flip_car=0
        
    def update(self):
        
        self.screen.fill((100,100,100))
        self.screen.blit(self.background,(0,0))
        
        
        
        for car in Bridge_Handler.bridge_handler().list_of_cars:
            
            if car.flip_car==1:
                self.flip_car_image(car)
                
            if car.state==State.CROSSING:
            
                if car.carX<=BRIDGE_LEFT_OFFSET:
                    car.carX = BRIDGE_LEFT_OFFSET
                    #car.carY = 380
                    
                if car.carX>=BRIDGE_RIGHT_OFFSET:
                    car.carX = BRIDGE_RIGHT_OFFSET
                    #car.carY = 380
                    
                car.carY=208    
            
            elif car.state==State.PARKED:
                self.park_car(car)
                
            elif car.state==State.WAITING or car.state==State.IN_LINE:
                self.car_in_line(car)
                
            status_car = self.base_font.render(car.car_status, True,(255,255,255))
            
            car_crossing_time = self.font_instr.render("T: " + str(car.crossing_time), True,(255,255,255))
            car_waiting_time = self.font_instr.render("P: " + str(car.waiting_time), True,(255,255,255))
            
            self.screen.blit(car_crossing_time, (car.carX+5,car.carY-4))
            self.screen.blit(car_waiting_time, (car.carX+5,car.carY-14))
            
            self.screen.blit(status_car, (80,465+car.Id*20))
            self.screen.blit(car.car_image,(car.carX,car.carY))
            
    
    def car_in_line(self,car):
        if car.car_direction==Direction.RIGHT:
            self.car_in_line_right(car)
        
        else:
            self.car_in_line_left(car)
    
    def car_in_line_left(self,car):
        car_index=Bridge.cars_l.index(car.Id)
        
        car.carY=208 
        car.carX=BRIDGE_LEFT_OFFSET-car_index*45-45
    
    def car_in_line_right(self,car):
        car_index=Bridge.cars_r.index(car.Id)
        
        car.carY=208 
        car.carX=BRIDGE_RIGHT_OFFSET+car_index*45+45
    
    def park_car(self,car):
        if car.car_direction==Direction.RIGHT:
            self.park_in_right_side(car)
        
        else:
            self.park_in_left_side(car)
    
    def park_in_left_side(self,car):
        if car.Id==0:
            car.carX=BRIDGE_LEFT_OFFSET-60
            car.carY=380
            
        elif car.Id==1:
            car.carX=BRIDGE_LEFT_OFFSET-60
            car.carY=380-50
            
        elif car.Id==2:
            car.carX=BRIDGE_LEFT_OFFSET-60
            car.carY=380-100
            
        elif car.Id==3:
            car.carX=BRIDGE_LEFT_OFFSET-60-80
            car.carY=380-300
            
        elif car.Id==4:
            car.carX=BRIDGE_LEFT_OFFSET-60-80
            car.carY=380-350
            
        elif car.Id==5:
            car.carX=BRIDGE_LEFT_OFFSET-60
            car.carY=380-250
            
        elif car.Id==6:
            car.carX=BRIDGE_LEFT_OFFSET-60
            car.carY=380-300
            
        elif car.Id==7:
            car.carX=BRIDGE_LEFT_OFFSET-60
            car.carY=380-350
            
        elif car.Id==8:
            car.carX=BRIDGE_LEFT_OFFSET-60-80
            car.carY=380
            
        elif car.Id==9:
            car.carX=BRIDGE_LEFT_OFFSET-60-80
            car.carY=380-50
        
    def park_in_right_side(self,car):
        if car.Id==0:
            car.carX=BRIDGE_RIGHT_OFFSET+20
            car.carY=380
            
        elif car.Id==1:
            car.carX=BRIDGE_RIGHT_OFFSET+20
            car.carY=380-50
            
        elif car.Id==2:
            car.carX=BRIDGE_RIGHT_OFFSET+20
            car.carY=380-100
            
        elif car.Id==3:
            car.carX=BRIDGE_RIGHT_OFFSET+20+80
            car.carY=380-300
            
        elif car.Id==4:
            car.carX=BRIDGE_RIGHT_OFFSET+20+80
            car.carY=380-250
            
        elif car.Id==5:
            car.carX=BRIDGE_RIGHT_OFFSET+20
            car.carY=380-250
            
        elif car.Id==6:
            car.carX=BRIDGE_RIGHT_OFFSET+20
            car.carY=380-300
            
        elif car.Id==7:
            car.carX=BRIDGE_RIGHT_OFFSET+20
            car.carY=380-350
            
        elif car.Id==8:
            car.carX=BRIDGE_RIGHT_OFFSET+20+80
            car.carY=380
            
        elif car.Id==9:
            car.carX=BRIDGE_RIGHT_OFFSET+20+80
            car.carY=380-50
            
    def verify_input_clicked(self,event):
        if self.txt_box_travessia.collidepoint(event.pos):
            self.active_travessia = True
            
        else:
            self.active_travessia = False
            
        if self.txt_box_espera.collidepoint(event.pos):
            self.active_espera = True
            
        else:
            self.active_espera = False
            
        if self.txt_box_direcao.collidepoint(event.pos):
            self.active_direcao = True
            
        else:
            self.active_direcao = False
            
        if self.txt_box_deletar.collidepoint(event.pos):
            self.active_deletar = True
            
        else:
            self.active_deletar = False
            
        if self.txt_box_ponte.collidepoint(event.pos):
            self.active_ponte = True
            self.txt_erro = ''
            
        else:
            self.active_ponte = False
            self.txt_erro = ''
            
    def create_car(self):
        print("Valores:")
        print(Bridge.left_mutex._value,Bridge.right_mutex._value,Bridge.bridge_semaphore._value)
        
        try:    
            if int(self.txt_input_espera) >= 0 and int(self.txt_input_espera) < 10000: 
                espera = int(self.txt_input_espera)
                self.txt_input_espera = ''
                
            else:
                self.txt_erro = 'Entrada inválida para Tempo de Espera, favor digitar números a partir de 0'
                self.txt_input_espera = ''
                espera = None
                
        except:
            print('String not allowed in Tempo de Travessia')
            espera = None
        try:
            if int(self.txt_input_travessia) >= 10 and int(self.txt_input_travessia) < 10000:
                travessia = int(self.txt_input_travessia)
                self.txt_input_travessia = ''
                
            else:
                self.txt_erro = 'Entrada inválida para Tempo de Travessia, favor digitar números de a partir de 10'
                self.txt_input_travessia = ''
                travessia = None
        except:
            print('String not allowed in Tempo de Espera')
            travessia = None
            
        if self.txt_input_direcao == 'Oeste-Leste' or self.txt_input_direcao == 'oeste-leste' or self.txt_input_direcao == 'Oeste-leste':
            direcao_carro = Direction.LEFT
            self.txt_input_direcao = ''
            
        elif self.txt_input_direcao == 'Leste-Oeste' or self.txt_input_direcao == 'leste-oeste' or self.txt_input_direcao == 'Leste-oeste':
            direcao_carro = Direction.RIGHT
            self.txt_input_direcao = ''
            
        else:
            self.txt_input_direcao = ''
            self.txt_erro = 'Entrada Inválida, favor escrever Leste-Oeste ou Oeste-Leste'
            direcao_carro = None
            
        if len(Bridge_Handler.bridge_handler().list_of_cars)>=10:
            return
            
        if travessia != None and espera != None and direcao_carro != None:
            print('Travessia'+str(travessia))
            print('Espera:'+str(espera))
            print('Direção:'+str(direcao_carro))
            Bridge_Handler.bridge_handler().append_car_to_bridge(espera, travessia, direcao_carro)
            self.gui_controller.append_to_log("Carro %d Criado" % Bridge_Handler.bridge_handler().list_of_cars[-1].Id)
            self.gui_controller.connect_object(Bridge_Handler.bridge_handler().list_of_cars[-1])
            Bridge_Handler.bridge_handler().list_of_cars[-1].start()
            
        else:
            print('unable to create a car, wrong input')
            
    def delete_car(self):
        try:
            if int(self.txt_input_deletar) >= 0 and int(self.txt_input_deletar) < 10:
                carro_deletar = int(self.txt_input_deletar)
                print('Carro Deletado: '+str(carro_deletar))
                self.txt_input_deletar = ''
                
            else:
                self.txt_erro = 'Entrada inválida, favor digitar números de 0 a 9'
                self.txt_input_deletar = ''
                carro_deletar = None
                
        except:
            self.txt_erro = 'Entrada inválida, favor digitar números de 0 a 9'
            self.txt_input_deletar = ''
            carro_deletar = None
        
        for car in Bridge_Handler.bridge_handler().list_of_cars:
            if car.Id==carro_deletar:
                
                self.gui_controller.append_to_log("Carro %d Deletado" % car.Id)
                
                Bridge_Handler.bridge_handler().list_of_cars.remove(car)
                car.is_running=False
                
                if car.state==State.CROSSING or car.state==State.IN_LINE:
                    if car.car_direction==Direction.LEFT:
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
                        
                    car.free_bridge_from_priority()
                    
                elif car.state==State.WAITING:
                    
                    
                    if car.car_direction==Direction.LEFT:
                        if Bridge.cars_l[0]==car.Id:
                            
                            if Bridge.left_mutex._value==0:
                                
                                Bridge.left_mutex.release()
                                
                            
                    else:
                        
                        if Bridge.cars_r[0]==car.Id:
                            if Bridge.right_mutex._value==0:
                                
                                Bridge.right_mutex.release()
                                
                    car.free_bridge_from_priority()
                        
                           
                try:
                    Bridge.cars_l.remove(car.Id)
                except:
                    pass
                try:
                    Bridge.cars_r.remove(car.Id)
                except:
                    pass
                        
                
                #print("Valores:")
                #print(Bridge.left_mutex._value,Bridge.right_mutex._value,Bridge.bridge_semaphore._value,Bridge.number_of_left,Bridge.number_of_right)
                
    def set_bridge_priority(self):
        direcao_ponte=Bridge.bridge().bridge_priority
        
        if self.txt_input_ponte == 'Oeste-Leste' or self.txt_input_ponte == 'oeste-leste' or self.txt_input_ponte == 'Oeste-leste':
            self.txt_input_ponte = ''
            self.txt_direcao_ponte = 'Direção da Ponte --->'
            direcao_ponte = Priority.LEFT
            print('Sentido da Ponte: '+direcao_ponte)
            
        elif self.txt_input_ponte == 'Leste-Oeste' or self.txt_input_ponte == 'leste-oeste' or self.txt_input_ponte == 'Leste-oeste':
            self.txt_input_ponte = ''
            self.txt_direcao_ponte = 'Direção da Ponte <---'
            direcao_ponte = Priority.RIGHT
            print('Sentido da Ponte: '+direcao_ponte)
            
        elif self.txt_input_ponte == 'nenhuma':
            self.txt_input_ponte = ''
            self.txt_direcao_ponte = 'Direção da Ponte NENHUMA'
            direcao_ponte = Priority.NONE
            print('Sentido da Ponte: '+direcao_ponte) 
            
        else:
            self.txt_input_ponte = ''
            self.txt_erro = 'Entrada Inválida, favor escrever Leste-Oeste ou Oeste-Leste'
            
        Bridge.bridge().bridge_priority=direcao_ponte
        
        for car in Bridge_Handler.bridge_handler().list_of_cars:
            car.free_bridge_from_priority()
            
    def get_keyboard_input(self,event):
        if self.active_travessia == True:
            if event.key == pygame.K_BACKSPACE:
                self.txt_input_travessia = self.txt_input_travessia[0:-1]
                
            else:
                self.txt_input_travessia += event.unicode
                
                
        if self.active_espera == True:  
            if event.key == pygame.K_BACKSPACE:
                self.txt_input_espera = self.txt_input_espera[0:-1]
                
            else:
                self.txt_input_espera += event.unicode
                
        if self.active_direcao == True:  
            if event.key == pygame.K_BACKSPACE:
                self.txt_input_direcao = self.txt_input_direcao[0:-1]
                
            else:
                self.txt_input_direcao += event.unicode
                
        if self.active_deletar == True:  
            if event.key == pygame.K_BACKSPACE:
                self.txt_input_deletar = self.txt_input_deletar[0:-1]
                
            else:
                self.txt_input_deletar += event.unicode
                
        if self.active_ponte == True:  
            if event.key == pygame.K_BACKSPACE:
                self.txt_input_ponte = self.txt_input_ponte[0:-1]
                
            else:
                self.txt_input_ponte += event.unicode
        
        
        
            