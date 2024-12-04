class ImgProducto:
    def __init__(self, p_id, p_img_nombre, p_imagen, p_imgPrincipal, p_PRODUCTOid):
        self.id = p_id
        self.img_nombre = p_img_nombre
        self.imagen = p_imagen
        self.imgPrincipal = p_imgPrincipal
        self.PRODUCTOid = p_PRODUCTOid

    def __str__(self):
        return (f"ImgProducto(id={self.id}, img_nombre='{self.img_nombre}', imagen='{self.imagen}', "
                f"imgPrincipal={self.imgPrincipal}, PRODUCTOid={self.PRODUCTOid})")

