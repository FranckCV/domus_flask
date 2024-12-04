class Comentario:
    def __init__(self, p_id, p_nombres, p_apellidos, p_email, p_celular, p_mensaje, 
                 p_fecha_registro, p_estado, p_MOTIVO_COMENTARIOid, p_USUARIOid):
        self.id = p_id
        self.nombres = p_nombres
        self.apellidos = p_apellidos
        self.email = p_email
        self.celular = p_celular
        self.mensaje = p_mensaje
        self.fecha_registro = p_fecha_registro
        self.estado = p_estado
        self.MOTIVO_COMENTARIOid = p_MOTIVO_COMENTARIOid
        self.USUARIOid = p_USUARIOid

    def __str__(self):
        return (f"Comentario(id={self.id}, nombres='{self.nombres}', apellidos='{self.apellidos}', "
                f"email='{self.email}', celular='{self.celular}', mensaje='{self.mensaje}', "
                f"fecha_registro='{self.fecha_registro}', estado='{self.estado}', "
                f"MOTIVO_COMENTARIOid={self.MOTIVO_COMENTARIOid}, USUARIOid={self.USUARIOid})")

