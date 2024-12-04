class ListaDeseos:
    def __init__(self, p_PRODUCTOid, p_USUARIOid):
        self.PRODUCTOid = p_PRODUCTOid
        self.USUARIOid = p_USUARIOid

    def __str__(self):
        return f"ListaDeseos(PRODUCTOid={self.PRODUCTOid}, USUARIOid={self.USUARIOid})"


