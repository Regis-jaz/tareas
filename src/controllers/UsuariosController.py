from models.UsuariosModel import UsuarioModel

class AuthController:
    def __init__(self):
        self.usuario_model = UsuarioModel()

    def login(self, email, password):
        try:
            user_db = self.usuario_model.validar_login(email, password)

            if not user_db:
                return None, "Correo o contraseña incorrectos"

            self.usuario_model.actualizar_ultimo_acceso(user_db["id_usuario"])
        
            user_db_actualizado = self.usuario_model.obtener_por_id(user_db["id_usuario"])

            user = {
                "id_usuario": user_db_actualizado["id_usuario"],
                "nombre": user_db_actualizado["nombre"],
                "apellido": user_db_actualizado["apellido"],
                "telefono": user_db_actualizado["telefono"],
                "email": user_db_actualizado["email"],
                "fecha_registro": user_db_actualizado["fecha_registro"],
                "ultimo_acceso": user_db_actualizado["ultimo_acceso"],  
        }

            return user, "Login exitoso 💗"
        
        except Exception as e:
            return None, f"Error en login: {str(e)}"
    
    def registrar(self, usuario_data):
        try:
            if self.usuario_model.email_existe(usuario_data.email):
                return False, "El correo electrónico ya está registrado 💗"
            exito = self.usuario_model.registrar(usuario_data)
            
            if exito:
                return True, "Usuario registrado exitosamente 💗"
            else:
                return False, "Error al registrar usuario"
                
        except Exception as e:
            return False, f"Error en registro: {str(e)}"