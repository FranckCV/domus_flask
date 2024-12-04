class Caracteristica:
    def __init__(self, p_id, p_campo, p_disponibilidad):
        self.id = p_id
        self.campo = p_campo
        self.disponibilidad = p_disponibilidad

    def __str__(self):
        return f"Caracteristica(id={self.id}, campo='{self.campo}', disponibilidad={self.disponibilidad})"




