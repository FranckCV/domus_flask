class Novedad:
    def __init__(self, p_id, p_nombre, p_titulo, p_fecha_inicio, p_fecha_vencimiento, p_terminos, 
                 p_fecha_registro, p_disponibilidad, p_MARCAid, p_SUBCATEGORIAid, p_TIPO_NOVEDADid):
        self.id = p_id
        self.nombre = p_nombre
        self.titulo = p_titulo
        self.fecha_inicio = p_fecha_inicio
        self.fecha_vencimiento = p_fecha_vencimiento
        self.terminos = p_terminos
        self.fecha_registro = p_fecha_registro
        self.disponibilidad = p_disponibilidad
        self.MARCAid = p_MARCAid
        self.SUBCATEGORIAid = p_SUBCATEGORIAid
        self.TIPO_NOVEDADid = p_TIPO_NOVEDADid

    def __str__(self):
        return (f"Novedad(id={self.id}, nombre='{self.nombre}', titulo='{self.titulo}', "
                f"fecha_inicio='{self.fecha_inicio}', fecha_vencimiento='{self.fecha_vencimiento}', "
                f"terminos='{self.terminos}', fecha_registro='{self.fecha_registro}', "
                f"disponibilidad={self.disponibilidad}, MARCAid={self.MARCAid}, "
                f"SUBCATEGORIAid={self.SUBCATEGORIAid}, TIPO_NOVEDADid={self.TIPO_NOVEDADid})")


