from PySide2 import QtCore

class GUI_Controller(QtCore.QObject):
    '''Sinais que comunicam com a thread da GUI'''
    object_connect_signal=QtCore.Signal(object)
    append_log_signal=QtCore.Signal(str)
    
    def __init__(self):
        super(GUI_Controller,self).__init__()
        
    def connect_object(self,car):
        self.object_connect_signal.emit(car)
        
    def append_to_log(self,text):
        self.append_log_signal.emit(text)
        
    
        
    