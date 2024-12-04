class DetallesPedido:
    def __init__(self, p_PRODUCTOid, p_PEDIDOid, p_cantidad):
        self.PRODUCTOid = p_PRODUCTOid
        self.PEDIDOid = p_PEDIDOid
        self.cantidad = p_cantidad

    def __str__(self):
        return f"DetallesPedido(PRODUCTOid={self.PRODUCTOid}, PEDIDOid={self.PEDIDOid}, cantidad={self.cantidad})"


