class Usuario:
    def __init__(self, p_id, p_nombres, p_apellidos, p_doc_identidad, p_img_usuario, p_genero,
                 p_fecha_nacimiento, p_telefono, p_correo, p_contrasenia, p_disponibilidad,
                 p_fecha_registro, p_TIPO_USUARIOid):
        self.id = p_id
        self.nombres = p_nombres
        self.apellidos = p_apellidos
        self.doc_identidad = p_doc_identidad
        self.img_usuario = p_img_usuario
        self.genero = p_genero
        self.fecha_nacimiento = p_fecha_nacimiento
        self.telefono = p_telefono
        self.correo = p_correo
        self.contrasenia = p_contrasenia
        self.disponibilidad = p_disponibilidad
        self.fecha_registro = p_fecha_registro
        self.TIPO_USUARIOid = p_TIPO_USUARIOid

    def __str__(self):
        return (f"Usuario(id={self.id}, nombres='{self.nombres}', apellidos='{self.apellidos}', "
                f"doc_identidad='{self.doc_identidad}', img_usuario='{self.img_usuario}', genero='{self.genero}', "
                f"fecha_nacimiento='{self.fecha_nacimiento}', telefono='{self.telefono}', "
                f"correo='{self.correo}', disponibilidad={self.disponibilidad}, "
                f"fecha_registro='{self.fecha_registro}', TIPO_USUARIOid={self.TIPO_USUARIOid})")

