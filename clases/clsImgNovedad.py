class ImgNovedad:
    def __init__(self, p_id, p_nomImagen, p_imagen, p_TIPO_IMG_NOVEDADid, p_NOVEDADid):
        self.id = p_id
        self.nomImagen = p_nomImagen
        self.imagen = p_imagen
        self.TIPO_IMG_NOVEDADid = p_TIPO_IMG_NOVEDADid
        self.NOVEDADid = p_NOVEDADid

    def __str__(self):
        return (f"ImgNovedad(id={self.id}, nomImagen='{self.nomImagen}', imagen='{self.imagen}', "
                f"TIPO_IMG_NOVEDADid={self.TIPO_IMG_NOVEDADid}, NOVEDADid={self.NOVEDADid})")




