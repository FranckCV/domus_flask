class Producto:
    def __init__(self, p_id, p_nombre, p_price_regular, p_precio_online, p_precio_oferta, p_info_adicional, 
                 p_stock, p_fecha_registro, p_disponibilidad, p_MARCAid, p_SUBCATEGORIAid):
        self.id = p_id
        self.nombre = p_nombre
        self.price_regular = p_price_regular
        self.precio_online = p_precio_online
        self.precio_oferta = p_precio_oferta
        self.info_adicional = p_info_adicional
        self.stock = p_stock
        self.fecha_registro = p_fecha_registro
        self.disponibilidad = p_disponibilidad
        self.MARCAid = p_MARCAid
        self.SUBCATEGORIAid = p_SUBCATEGORIAid

    def __str__(self):
        return (f"Producto(id={self.id}, nombre='{self.nombre}', price_regular={self.price_regular}, "
                f"precio_online={self.precio_online}, precio_oferta={self.precio_oferta}, "
                f"info_adicional='{self.info_adicional}', stock={self.stock}, "
                f"fecha_registro='{self.fecha_registro}', disponibilidad={self.disponibilidad}, "
                f"MARCAid={self.MARCAid}, SUBCATEGORIAid={self.SUBCATEGORIAid})")

