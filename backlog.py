#generacion de reservas o booking
import datetime
from client import User
from exeption import IsNotUserRegistered, InvalidBacklog, ValidationError
from logger import Logger


class Backlog():

    def __init__(self, logger: Logger = None):
        #Contenedor de las reservas
        self.items=[]
        self.logger = logger or Logger()
        self.logger.log_info("Backlog inicializado")

    def _buscar_usuario(self, user_id:int):
        usuario = User.obtener_usuario_por_id(user_id)
        if usuario is None:
            self.logger.log_error(f"Usuario no encontrado en backlog: ID={user_id}")
            raise IsNotUserRegistered(f"El usuario con ID {user_id} no existe")
        self.logger.log_info(f"Usuario validado en backlog: ID={user_id}")
        return usuario

    def addBacklog(self, user_id:int, reserva:str, mensaje:str="", hora:str=""):
        if not reserva:
            self.logger.log_error("Intento de crear reserva vacía")
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
        self.logger.log_info(
            f"Reserva creada: reservation_id={item['reservation_id']}, user_id={user_id}"
        )
        return item
    #Metodo para mostrar todas las reservas
    def all(self):
        self.logger.log_info(f"Consulta de todas las reservas: total={len(self.items)}")
        return list(self.items)
    #Metodo para buscar una reserva por usuario
    def find_by_user_id(self,user_id:int):
        self._buscar_usuario(user_id)
        reservas = [item for item in self.items if item["user_id"] == user_id]
        self.logger.log_info(
            f"Consulta de reservas por usuario: user_id={user_id}, total={len(reservas)}"
        )
        return reservas

    def update_hour(self, reservation_id:int, nueva_hora:str):
        if not nueva_hora:
            self.logger.log_error("Intento de actualizar reserva con hora vacía")
            raise ValidationError("La nueva hora no puede estar vacía")

        for item in self.items:
            if item["reservation_id"] == reservation_id:
                item["hora"] = nueva_hora
                item["estado"] = "reprogramada"
                item["updated_at"] = datetime.datetime.now()
                self.logger.log_warning(
                    f"Reserva reprogramada: reservation_id={reservation_id}, nueva_hora={nueva_hora}"
                )
                return item

        self.logger.log_error(f"No existe reserva para actualizar: ID={reservation_id}")
        raise InvalidBacklog(f"No existe una reserva con ID {reservation_id}")
            
    