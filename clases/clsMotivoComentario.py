class MotivoComentario:
    def __init__(self, p_id, p_motivo, p_disponibilidad):
        self.id = p_id
        self.motivo = p_motivo
        self.disponibilidad = p_disponibilidad

    def __str__(self):
        return f"MotivoComentario(id={self.id}, motivo='{self.motivo}', disponibilidad={self.disponibilidad})"

