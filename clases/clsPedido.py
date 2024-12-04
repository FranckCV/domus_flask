class Pedido:
    def __init__(self, p_id, p_fecha_compra, p_subtotal, p_METODO_PAGOid, p_USUARIOid, p_ESTADO_PEDIDOid):
        self.id = p_id
        self.fecha_compra = p_fecha_compra
        self.subtotal = p_subtotal
        self.METODO_PAGOid = p_METODO_PAGOid
        self.USUARIOid = p_USUARIOid
        self.ESTADO_PEDIDOid = p_ESTADO_PEDIDOid

    def __str__(self):
        return (f"Pedido(id={self.id}, fecha_compra='{self.fecha_compra}', subtotal={self.subtotal}, "
                f"METODO_PAGOid={self.METODO_PAGOid}, USUARIOid={self.USUARIOid}, "
                f"ESTADO_PEDIDOid={self.ESTADO_PEDIDOid})")
