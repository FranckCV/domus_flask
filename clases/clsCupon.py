
class Cupon:
    def __init__(self, p_id, p_codigo, p_fecha_registro, p_fecha_inicio, p_fecha_vencimiento, p_cant_descuento):
        self.id = p_id
        self.codigo = p_codigo
        self.fecha_registro = p_fecha_registro
        self.fecha_inicio = p_fecha_inicio
        self.fecha_vencimiento = p_fecha_vencimiento
        self.cant_descuento = p_cant_descuento

    def __str__(self):
        return (f"Cupon(id={self.id}, codigo='{self.codigo}', fecha_registro='{self.fecha_registro}', "
                f"fecha_inicio='{self.fecha_inicio}', fecha_vencimiento='{self.fecha_vencimiento}', "
                f"cant_descuento={self.cant_descuento})")













