#Servicio de los modulos
from backlog import Backlog
from client import User
from consultoria import ConsultoriaEstrategica, ConsultoriaGeneral, ConsultoriaTecnica
from logger import FileLogger, Logger


class UserService:
    def __init__(self, logger: Logger = None, backlog: Backlog = None):
        self.logger = logger or FileLogger()
        self.backlog = backlog or Backlog(self.logger)
        self.servicios = []
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

    def crear_reserva(
        self,
        user_id: int,
        reserva: str,
        mensaje: str = "",
        hora: str = "",
        servicio: str = "",
    ) -> dict:
        try:
            item = self.backlog.addBacklog(user_id, reserva, mensaje, hora, servicio)
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

    def crear_servicio_consultoria(self, tipo: str, nombre: str, precio_base: float) -> dict:
        tipo_normalizado = (tipo or "").strip().lower()

        if tipo_normalizado == "general":
            servicio = ConsultoriaGeneral(nombre, precio_base)
        elif tipo_normalizado == "tecnica":
            servicio = ConsultoriaTecnica(nombre, precio_base)
        elif tipo_normalizado == "estrategica":
            servicio = ConsultoriaEstrategica(nombre, precio_base)
        else:
            raise ValueError("Tipo de servicio no válido. Usa: general, tecnica o estrategica")

        resumen = servicio.obtener_resumen()
        self.servicios.append(servicio)
        self.logger.log_info(
            f"Servicio consultivo creado: ID={resumen['id_servicio']}, tipo={resumen['tipo']}"
        )
        return resumen

    def obtener_servicios(self) -> list:
        return [servicio.obtener_resumen() for servicio in self.servicios]

    def obtener_servicio_por_id(self, service_id: int):
        for servicio in self.servicios:
            if servicio.id_servicio == service_id:
                return servicio
        return None

    def obtener_resumen_reportes(self) -> dict:
        usuarios = User.obtener_todos_usuarios()
        reservas = self.obtener_reservas()
        servicios = self.obtener_servicios()

        pendientes = sum(1 for reserva in reservas if reserva.get("estado") == "pendiente")
        reprogramadas = sum(1 for reserva in reservas if reserva.get("estado") == "reprogramada")

        return {
            "total_usuarios": len(usuarios),
            "total_reservas": len(reservas),
            "total_servicios": len(servicios),
            "reservas_pendientes": pendientes,
            "reservas_reprogramadas": reprogramadas,
            "usuarios": usuarios,
            "reservas": reservas,
            "servicios": servicios,
        }