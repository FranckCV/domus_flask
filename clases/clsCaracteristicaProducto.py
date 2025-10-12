class CaracteristicasProducto:
    def __init__(self, p_CARACTERISTICAid, p_PRODUCTOid, p_valor, p_principal):
        self.CARACTERISTICAid = p_CARACTERISTICAid
        self.PRODUCTOid = p_PRODUCTOid
        self.valor = p_valor
        self.principal = p_principal

    def __str__(self):
        return (f"CaracteristicasProducto(CARACTERISTICAid={self.CARACTERISTICAid}, "
                f"PRODUCTOid={self.PRODUCTOid}, valor='{self.valor}', principal={self.principal})")

