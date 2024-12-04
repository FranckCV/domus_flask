class TipoUsuario:
    def __init__(self, p_id, p_tipo, p_imagen, p_descripcion, p_disponibilidad):
        self.id = p_id
        self.tipo = p_tipo
        self.imagen = p_imagen
        self.descripcion = p_descripcion
        self.disponibilidad = p_disponibilidad

    def __str__(self):
        return (f"TipoUsuario(id={self.id}, tipo='{self.tipo}', imagen='{self.imagen}', "
                f"descripcion='{self.descripcion}', disponibilidad={self.disponibilidad})")





