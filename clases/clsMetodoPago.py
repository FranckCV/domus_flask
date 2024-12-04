class MetodoPago:
    def __init__(self, p_id, p_metodo, p_disponibilidad):
        self.id = p_id
        self.metodo = p_metodo
        self.disponibilidad = p_disponibilidad

    def __str__(self):
        return f"MetodoPago(id={self.id}, metodo='{self.metodo}', disponibilidad={self.disponibilidad})"

