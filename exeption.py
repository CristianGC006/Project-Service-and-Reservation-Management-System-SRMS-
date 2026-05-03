#exepciones
from datetime import datetime
class CustomExeptions(Exception):
    def __init__(self, message):
        self.message=message
        self.date=datetime.now().strftime("%Y-%m-%d %H:%M")
        super().__init__(self.message)


    def __str__(self):
        return f"[{self.date} ERROR DEL SISTEMA: {self.message}]"
    
class IsUserRegistered(CustomExeptions):
    def __str__(self):
        return f"[{self.date} OPERACION NO PERMITIDA {self.message}]"

class IsNotUserRegistered(CustomExeptions):
    def __str__(self):
        return f"[{self.date} CLIENTE NO ENCONTRADO {self.message}]"

class AvialableService(CustomExeptions):
    def __str__(self):
        return f"[{self.date} SERVICIO NO DISPONIBLE {self.message}]"
    
class InvalidBacklog(CustomExeptions):
    def __str__(self):
        return f"[{self.date} RESERVA INVALIDA {self.message}]"
    
class ValidationError(CustomExeptions):
    def __str__(self):
        return f"[{self.date} ERROR DE VALIDACION {self.message}]"   