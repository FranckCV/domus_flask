class Subcategoria:
    def __init__(self, p_id, p_subcategoria, p_faicon_subcat, p_disponibilidad, p_CATEGORIAid):
        self.id = p_id
        self.subcategoria = p_subcategoria
        self.faicon_subcat = p_faicon_subcat
        self.disponibilidad = p_disponibilidad
        self.CATEGORIAid = p_CATEGORIAid

    def __str__(self):
        return (f"Subcategoria(id={self.id}, subcategoria='{self.subcategoria}', "
                f"faicon_subcat='{self.faicon_subcat}', disponibilidad={self.disponibilidad}, "
                f"CATEGORIAid={self.CATEGORIAid})")


