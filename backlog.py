#generacion de reservas o booking
import datetime
from client import User
from exeption import IsNotUserRegistered, InvalidBacklog, ValidationError
class Backlog():

    def __init__(self):
        #Contenedor de las reservas
        self.items=[]

    def _buscar_usuario(self, user_id:int):
        usuario = User.obtener_usuario_por_id(user_id)
        if usuario is None:
            raise IsNotUserRegistered(f"El usuario con ID {user_id} no existe")
        return usuario

    def addBacklog(self, user_id:int, reserva:str, mensaje:str="", hora:str=""):
        if not reserva:
            raise InvalidBacklog("La reserva no puede estar vacía")

        usuario = self._buscar_usuario(user_id)

        item={
            "reservation_id": len(self.items) + 1,
            "user_id": usuario["Id"],
            "name": usuario["name"],
            "email": usuario["email"],
            "phone": usuario["Phone"],
            "reserva": reserva,
            "mensaje": mensaje,
            "hora": hora if hora else datetime.datetime.now().strftime("%H:%M"),
            "date":datetime.datetime.now(),
            "estado":"pendiente"    
        }
        self.items.append(item)
        return item
    #Metodo para mostrar todas las reservas
    def all(self):
        return list(self.items)
    #Metodo para buscar una reserva por usuario
    def find_by_user_id(self,user_id:int):
        self._buscar_usuario(user_id)
        return [item for item in self.items if item["user_id"] == user_id]

    def update_hour(self, reservation_id:int, nueva_hora:str):
        if not nueva_hora:
            raise ValidationError("La nueva hora no puede estar vacía")

        for item in self.items:
            if item["reservation_id"] == reservation_id:
                item["hora"] = nueva_hora
                item["estado"] = "reprogramada"
                item["updated_at"] = datetime.datetime.now()
                return item

        raise InvalidBacklog(f"No existe una reserva con ID {reservation_id}")
            
    