#Generacion del client
class User():
    # Variable de clase para contar usuarios automáticamente
    _contador = 0
    # Lista de clase para almacenar todos los usuarios
    usuarios_registrados = []
    
    def __init__(self, name:str, email:str, phone:int):
        self.name = name
        self.email = email
        self.phone = phone
        # Incrementar el contador y asignar ID automáticamente
        User._contador += 1
        self.idUser = User._contador
    
    def create_User(self) -> dict:
        if not self.name:
            raise ValueError("El nombre de usuario no puede estar Vacio")
        if "@" not in self.email:
            raise ValueError("Email inválido")
        
        # Crear diccionario con los datos del usuario
        usuario_dict = {
            "name": self.name,
            "email": self.email,
            "Phone": self.phone,
            "Id": self.idUser
        }
        
        # Agregar el usuario a la lista de usuarios registrados
        User.usuarios_registrados.append(usuario_dict)
        
        return usuario_dict
    
    @classmethod
    def obtener_todos_usuarios(cls) -> list:
        """Retorna la lista de todos los usuarios registrados"""
        return cls.usuarios_registrados

    @classmethod
    def obtener_usuario_por_id(cls, user_id: int):
        for usuario in cls.usuarios_registrados:
            if usuario["Id"] == user_id:
                return usuario
        return None
    

    
if __name__ == "__main__":
    #Ejemplo
    U1 = User("Rocio", "Rocio@gmail.com", 123456)
    U2 = User("Juan", "Juan@gmail.com", 654321)
    U3 = User("María", "Maria@gmail.com", 111222)

    registro1 = U1.create_User()
    registro2 = U2.create_User()
    registro3 = U3.create_User()

    print("Usuario 1:", registro1)
    print("Usuario 2:", registro2)
    print("Usuario 3:", registro3)
    print("\nTodos los usuarios registrados:")
    print(User.obtener_todos_usuarios())

