# conexion.py - Mejorado

import sqlite3
import os

class Comunicacion:
    def __init__(self):
        ruta_db = os.path.join(os.path.dirname(__file__), 'juegos_ps3.db')
        if not os.path.exists(ruta_db):
            raise FileNotFoundError(f"Base de datos no encontrada: {ruta_db}")
        self.conexion = sqlite3.connect(ruta_db)
        self.cursor = self.conexion.cursor()
    
    def obtener_generos(self):
        """Obtiene la lista de géneros disponibles"""
        self.cursor.execute("SELECT DISTINCT genero FROM juegos_ps3 ORDER BY genero")
        return [g[0] for g in self.cursor.fetchall()]
    
    def obtener_años_disponibles(self):
        """Obtiene los años disponibles en la base de datos"""
        self.cursor.execute("SELECT DISTINCT anio_lanzamiento FROM juegos_ps3 ORDER BY anio_lanzamiento DESC")
        return [str(a[0]) for a in self.cursor.fetchall()]
    
    def obtener_juegos_por_genero(self, genero):
        """Obtiene juegos filtrados por género"""
        self.cursor.execute("""
            SELECT id, titulo, descripcion, genero, plataforma, anio_lanzamiento, precio_aproximado, imagen_juego
            FROM juegos_ps3 WHERE genero = ? ORDER BY titulo
        """, (genero,))
        return self.cursor.fetchall()
    
    def buscar_juego_por_titulo(self, titulo):
        """Busca juegos por título (búsqueda parcial)"""
        self.cursor.execute("""
            SELECT id, titulo, descripcion, genero, plataforma, anio_lanzamiento, precio_aproximado, imagen_juego
            FROM juegos_ps3 WHERE titulo LIKE ? ORDER BY titulo
        """, ('%' + titulo + '%',))
        return self.cursor.fetchall()
    
    def obtener_juegos_por_anio(self, anio):
        """Obtiene juegos filtrados por año"""
        self.cursor.execute("""
            SELECT id, titulo, descripcion, genero, plataforma, anio_lanzamiento, precio_aproximado, imagen_juego
            FROM juegos_ps3 WHERE anio_lanzamiento = ? ORDER BY titulo
        """, (anio,))
        return self.cursor.fetchall()
    
    def insertar_imagen_juego(self, juego_id, ruta_imagen):
        """Inserta/actualiza la imagen de un juego"""
        try:
            with open(ruta_imagen, 'rb') as archivo:
                imagen_binaria = archivo.read()
            self.cursor.execute("UPDATE juegos_ps3 SET imagen_juego = ? WHERE id = ?", (imagen_binaria, juego_id))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al insertar imagen: {e}")
            return False
    
    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        try:
            self.cursor.close()
            self.conexion.close()
        except:
            pass