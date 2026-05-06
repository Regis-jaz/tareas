from models.TareasModel import TareaModel

class TareaController:
    def __init__(self):
        self.model = TareaModel()
    
    def obtener_lista(self, id_usuario):
        return self.model.listar_por_usuario(id_usuario)
    
    def guardar_nueva(self, id_usuario, titulo, desc, prio, clas, estado, 
                    fecha_limite=None, hora_limite=None):
        if not titulo:
            return False, "El título es obligatorio"
        
        self.model.crear(id_usuario, titulo, desc, prio, clas, estado, 
                        fecha_limite, hora_limite)
        return True, "Tarea guardada 💗"
    
    def eliminar_tarea(self, id_tarea):
        try:
            self.model.eliminar(id_tarea)
            return True, "Tarea eliminada 💗"
        except Exception as e:
            return False, str(e)