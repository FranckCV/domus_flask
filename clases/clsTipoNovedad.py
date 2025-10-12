class TipoNovedad:
    def __init__(self, p_id, p_nomTipo, p_disponibilidad):
        self.id = p_id
        self.nomTipo = p_nomTipo
        self.disponibilidad = p_disponibilidad

    def __str__(self):
        return f"TipoNovedad(id={self.id}, nomTipo='{self.nomTipo}', disponibilidad={self.disponibilidad})"


