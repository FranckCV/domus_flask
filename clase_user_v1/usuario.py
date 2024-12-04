class Usuario:
    def __init__(self, id, nombres=None, apellidos=None, doc_identidad=None, img_usuario=None, 
                 genero=None, fecha_nacimiento=None, telefono=None, correo=None, 
                 contrasenia=None, disponibilidad=None, fecha_registro=None, 
                 tipo_usuario_id=None):
        self.id = id
        self.nombres = nombres
        self.apellidos = apellidos
        self.doc_identidad = doc_identidad
        self.img_usuario = img_usuario
        self.genero = genero
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.correo = correo
        self.contrasenia = contrasenia
        self.disponibilidad = disponibilidad
        self.fecha_registro = fecha_registro
        self.tipo_usuario_id = tipo_usuario_id

    def to_dict(self):
        return {'id': self.id, "correo": self.correo} 

    def __str__(self):
        return (
            f"Usuario(id='{self.id}', nombres='{self.nombres}', apellidos='{self.apellidos}', "
            f"correo='{self.correo}', tipo_usuario_id='{self.tipo_usuario_id}')"
        )
