class Marca:
    def __init__(self, p_id, p_marca, p_img_logo, p_img_banner, p_fecha_registro, p_disponibilidad):
        self.id = p_id
        self.marca = p_marca
        self.img_logo = p_img_logo
        self.img_banner = p_img_banner
        self.fecha_registro = p_fecha_registro
        self.disponibilidad = p_disponibilidad

    def __str__(self):
        return (f"Marca(id={self.id}, marca='{self.marca}', img_logo='{self.img_logo}', "
                f"img_banner='{self.img_banner}', fecha_registro='{self.fecha_registro}', "
                f"disponibilidad={self.disponibilidad})")
