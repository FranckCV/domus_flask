class InformacionDomus:
    def __init__(self, p_id, p_correo, p_numero, p_imgLogo, p_imgIcon, p_descripcion, 
                 p_historia, p_vision, p_valores, p_mision):
        self.id = p_id
        self.correo = p_correo
        self.numero = p_numero
        self.imgLogo = p_imgLogo
        self.imgIcon = p_imgIcon
        self.descripcion = p_descripcion
        self.historia = p_historia
        self.vision = p_vision
        self.valores = p_valores
        self.mision = p_mision

    def __str__(self):
        return (f"InformacionDomus(id={self.id}, correo='{self.correo}', numero='{self.numero}', "
                f"imgLogo='{self.imgLogo}', imgIcon='{self.imgIcon}', descripcion='{self.descripcion}', "
                f"historia='{self.historia}', vision='{self.vision}', valores='{self.valores}', "
                f"mision='{self.mision}')")












