class EstadoPedido:
    def __init__(self, p_id, p_nomEstado):
        self.id = p_id
        self.nomEstado = p_nomEstado

    def __str__(self):
        return f"EstadoPedido(id={self.id}, nomEstado='{self.nomEstado}')"

