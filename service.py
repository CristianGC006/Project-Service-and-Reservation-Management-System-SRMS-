#Servicio de los modulos
from backlog import Backlog
from client import User
from logger import FileLogger, Logger


class UserService:
    def __init__(self, logger: Logger = None, backlog: Backlog = None):
        self.logger = logger or FileLogger()
        self.backlog = backlog or Backlog(self.logger)
        self.logger.log_info("UserService inicializado")

    def registrar_usuario(self, name: str, email: str, phone: int) -> dict:
        try:
            user = User(name, email, phone, logger=self.logger)
            usuario_registrado = user.create_User()
            self.logger.log_info(
                f"Usuario registrado desde service: ID={usuario_registrado['Id']}"
            )
            return usuario_registrado
        except Exception as error:
            self.logger.log_error(f"Error al registrar usuario desde service: {error}")
            raise

    def crear_reserva(self, user_id: int, reserva: str, mensaje: str = "", hora: str = "") -> dict:
        try:
            item = self.backlog.addBacklog(user_id, reserva, mensaje, hora)
            self.logger.log_info(
                f"Reserva creada desde service: reservation_id={item['reservation_id']}"
            )
            return item
        except Exception as error:
            self.logger.log_error(f"Error al crear reserva desde service: {error}")
            raise

    def obtener_reservas(self) -> list:
        return self.backlog.all()

    def obtener_reservas_por_usuario(self, user_id: int) -> list:
        return self.backlog.find_by_user_id(user_id)

    def actualizar_hora_reserva(self, reservation_id: int, nueva_hora: str) -> dict:
        try:
            return self.backlog.update_hour(reservation_id, nueva_hora)
        except Exception as error:
            self.logger.log_error(f"Error al actualizar reserva desde service: {error}")
            raise