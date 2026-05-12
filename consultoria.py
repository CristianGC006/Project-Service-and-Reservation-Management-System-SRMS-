from abc import ABC, abstractmethod


class ServicioConsultoria(ABC):
    _contador = 0

    def __init__(self, nombre: str, precio_base: float):
        ServicioConsultoria._contador += 1
        self.id_servicio = ServicioConsultoria._contador
        self.nombre = nombre.strip()
        self.precio_base = float(precio_base)

    @abstractmethod
    def calcular_costo(self, horas: float) -> float:
        raise NotImplementedError

    @abstractmethod
    def descripcion(self) -> str:
        raise NotImplementedError

    def obtener_resumen(self) -> dict:
        return {
            "id_servicio": self.id_servicio,
            "nombre": self.nombre,
            "precio_base": self.precio_base,
            "tipo": self.__class__.__name__,
            "descripcion": self.descripcion(),
        }


class ConsultoriaGeneral(ServicioConsultoria):
    def calcular_costo(self, horas: float) -> float:
        costo = self.precio_base * float(horas)
        if horas >= 5:
            costo *= 0.9
        return round(costo, 2)

    def descripcion(self) -> str:
        return "Consultoría general para análisis, orientación y acompañamiento básico."


class ConsultoriaTecnica(ServicioConsultoria):
    def calcular_costo(self, horas: float) -> float:
        costo = self.precio_base * float(horas) * 1.15
        return round(costo, 2)

    def descripcion(self) -> str:
        return "Consultoría técnica enfocada en diagnóstico, soporte y soluciones especializadas."


class ConsultoriaEstrategica(ServicioConsultoria):
    def calcular_costo(self, horas: float) -> float:
        costo = self.precio_base * float(horas)
        if horas >= 3:
            costo *= 0.85
        return round(costo, 2)

    def descripcion(self) -> str:
        return "Consultoría estratégica para planificación, mejora y toma de decisiones."