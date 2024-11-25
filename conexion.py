
import sqlite3
import os
class Comunicacion:
    def __init__(self):
        # Construimos la ruta completa al archivo de base de datos
        ruta_base_datos = os.path.join(os.path.dirname(__file__), 'juegos_ps3.db')
        if not os.path.exists(ruta_base_datos):
            raise FileNotFoundError(f"No se encontró la base de datos en {ruta_base_datos}")
        self.conexion = sqlite3.connect(ruta_base_datos)
    
    def obtener_generos(self):
        # Obtiene la lista de géneros de la base de datos
        cursor = self.conexion.cursor()
        cursor.execute("SELECT DISTINCT genero FROM juegos_ps3")
        generos = cursor.fetchall()
        return [genero[0] for genero in generos]

    def obtener_juegos_por_genero(self, genero):
        # Obtiene los juegos filtrados por género (solo columnas relevantes)
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT id, titulo, descripcion, genero, plataforma, anio_lanzamiento, precio_aproximado, imagen_juego
            FROM juegos_ps3
            WHERE genero = ?
        """, (genero,))
        return cursor.fetchall()

    def buscar_juego_por_titulo(self, titulo):
        # Busca juegos por título (solo columnas relevantes)
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT id, titulo, descripcion, genero, plataforma, anio_lanzamiento, precio_aproximado, imagen_juego
            FROM juegos_ps3
            WHERE titulo LIKE ?
        """, ('%' + titulo + '%',))
        return cursor.fetchall()

    def obtener_juegos_por_anio(self, anio_lanzamiento):
        # Obtiene los juegos filtrados por año de lanzamiento (solo columnas relevantes)
        cursor = self.conexion.cursor()
        cursor.execute("""
            SELECT id, titulo, descripcion, genero, plataforma, anio_lanzamiento, precio_aproximado, imagen_juego
            FROM juegos_ps3
            WHERE anio_lanzamiento = ?
        """, (anio_lanzamiento,))
        return cursor.fetchall()

    def insertar_imagen_juego(self, juego_id, ruta_imagen):
        # Inserta o actualiza la imagen del juego
        with open(ruta_imagen, 'rb') as archivo_imagen:
            imagen_binaria = archivo_imagen.read()

        cursor = self.conexion.cursor()
        cursor.execute('''UPDATE juegos_ps3 SET imagen_juego = ? WHERE id = ?''', (imagen_binaria, juego_id))
        self.conexion.commit()

    def cerrar_conexion(self):
        # Cierra la conexión con la base de datos
        self.conexion.close()
