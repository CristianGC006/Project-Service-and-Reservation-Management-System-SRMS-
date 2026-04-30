#Generacion del cliente
class User():
    def __init__(self, name:str,email:str,phone:int):
        self.name=name
        self.email=email
        self.phone=phone

    def create_User(self)->dict:
        if not self.name:
            raise ValueError("El nombre de usuario no puede estar Vacio")
        if "@" not in self.email:
            raise ValueError("Email inválido")
        return{"name":self.name,"email":self.email, "Phone":self.phone }
    
#Ejemplo
U=User("Rocio","Rocio@gmail.com", 123456)
registro=U.create_User()
print(registro)