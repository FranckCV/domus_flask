class Categoria:
    def __init__(self, p_id, p_categoria, p_faicon_cat, p_disponibilidad):
        self.id = p_id
        self.categoria = p_categoria
        self.faicon_cat = p_faicon_cat
        self.disponibilidad = p_disponibilidad

    def __str__(self):
        return (f"Categoria(id={self.id}, categoria='{self.categoria}', "
                f"faicon_cat='{self.faicon_cat}', disponibilidad={self.disponibilidad})")
