from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


class Logger(ABC):
    @abstractmethod
    def log_evento(self, nivel: str, mensaje: str) -> str:
        pass

    @abstractmethod
    def log_info(self, mensaje: str) -> str:
        pass

    @abstractmethod
    def log_error(self, mensaje: str) -> str:
        pass

    @abstractmethod
    def log_warning(self, mensaje: str) -> str:
        pass


class FileLogger(Logger):
    def __init__(self, file_path: str = "logs.txt"):
        self.file_path = Path(file_path)
        self.file_path.touch(exist_ok=True)

    def log_evento(self, nivel: str, mensaje: str) -> str:
        if not mensaje or not mensaje.strip():
            raise ValueError("El mensaje no puede estar vacío")

        nivel_normalizado = (nivel or "INFO").strip().upper()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        registro = f"[{timestamp}] {nivel_normalizado} - {mensaje.strip()}"

        with self.file_path.open("a", encoding="utf-8") as archivo:
            archivo.write(registro + "\n")

        print(registro)
        return registro

    def log_info(self, mensaje: str) -> str:
        return self.log_evento("INFO", mensaje)

    def log_error(self, mensaje: str) -> str:
        return self.log_evento("ERROR", mensaje)

    def log_warning(self, mensaje: str) -> str:
        return self.log_evento("WARNING", mensaje)


class logger(FileLogger):
    pass