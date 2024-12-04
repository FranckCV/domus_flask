class TipoImgNovedad:
    def __init__(self, p_id, p_tipo, p_disponibilidad):
        self.id = p_id
        self.tipo = p_tipo
        self.disponibilidad = p_disponibilidad

    def __str__(self):
        return f"TipoImgNovedad(id={self.id}, tipo='{self.tipo}', disponibilidad={self.disponibilidad})"



