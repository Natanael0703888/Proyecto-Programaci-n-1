class Juego:
    """Representa un juego de PS3"""
    
    def __init__(self, datos_tupla):
        """Crea un Juego desde una tupla de la base de datos"""
        self.id = datos_tupla[0]
        self.titulo = datos_tupla[1]
        self.descripcion = datos_tupla[2]
        self.anio = datos_tupla[3]
        self.precio = datos_tupla[4]
        self.imagen = datos_tupla[5]
        self.generos = datos_tupla[6] if len(datos_tupla) > 6 else ""
    
    @property
    def titulo_corto(self):
        """Título acortado para mostrar"""
        if len(self.titulo) > 22:
            return self.titulo[:22] + "..."
        return self.titulo
    
    @property
    def precio_formateado(self):
        """Precio formateado como moneda"""
        if self.precio is None:
            return "No disponible"
        try:
            return f"${float(self.precio):.2f} USD"
        except:
            return "No disponible"