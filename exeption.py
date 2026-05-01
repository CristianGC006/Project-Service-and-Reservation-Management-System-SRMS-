#exepciones
from datetime import datetime
class CustomExeptions(Exception):
    def __int__(self, mensaje):
        self.mensaje=mensaje
        self.date=datetime.now().strftime("%Y-%m-%d %H:%M")
        super().__init__(self.mensaje)

    
    
    pass