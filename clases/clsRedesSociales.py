class RedesSociales:
    def __init__(self, p_id, p_nomRed, p_faicon_red, p_enlace):
        self.id = p_id
        self.nomRed = p_nomRed
        self.faicon_red = p_faicon_red
        self.enlace = p_enlace

    def __str__(self):
        return f"RedesSociales(id={self.id}, nomRed='{self.nomRed}', faicon_red='{self.faicon_red}', enlace='{self.enlace}')"



