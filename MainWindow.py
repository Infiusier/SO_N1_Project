from PySide2.QtWidgets import *
from PySide2 import QtWidgets, QtCore    
from PySide2.QtCore import *
from Log import Ui_Log
from application import Application

class MainLog(QtWidgets.QMainWindow,Ui_Log,QtCore.QObject):
    
    def __init__(self):
        super(MainLog,self).__init__()
        self.setupUi(self)
        self.application=Application()
        
        self.textEdit.setReadOnly(True)
        
        self.application.screen.gui_controller.object_connect_signal.connect(self.connect_object)
        self.application.screen.gui_controller.append_log_signal.connect(self.append_to_log)
        self.application.start()
        
        
    def append_to_log(self,text):
        self.textEdit.append(text)
        
    def connect_object(self,car):
        car.gui_controller.append_log_signal.connect(self.append_to_log)
        