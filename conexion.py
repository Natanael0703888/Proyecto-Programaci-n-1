import sqlite3
import os
from Juego_model import Juego

class Comunicacion:
    def __init__(self):
        ruta_db = os.path.join(os.path.dirname(__file__), 'juegos_ps3.db')
        if not os.path.exists(ruta_db):
            raise FileNotFoundError(f"Base de datos no encontrada: {ruta_db}")
        self.conexion = sqlite3.connect(ruta_db)
        self.cursor = self.conexion.cursor()
    
    def _ejecutar_consulta(self, query, params=None):
        """Ejecuta una consulta y retorna los resultados como objetos Juego"""
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query) 
        
        resultados = self.cursor.fetchall()
        return [Juego(r) for r in resultados]
    
    def obtener_generos(self):
        """Obtiene la lista de géneros disponibles"""
        self.cursor.execute("SELECT nombre FROM generos ORDER BY nombre")
        return [g[0] for g in self.cursor.fetchall()]
    
    def obtener_años_disponibles(self):
        """Obtiene los años disponibles"""
        self.cursor.execute("""
            SELECT DISTINCT anio_lanzamiento 
            FROM juegos 
            WHERE anio_lanzamiento IS NOT NULL 
            ORDER BY anio_lanzamiento DESC
        """)
        return [str(a[0]) for a in self.cursor.fetchall()]
    
    def obtener_juegos_por_genero(self, genero):
        """Obtiene juegos filtrados por género"""
        query = """
        SELECT 
            j.id, j.titulo, j.descripcion, j.anio_lanzamiento, 
            j.precio, j.imagen_ruta,
            GROUP_CONCAT(g.nombre, ', ') as generos
        FROM juegos j
        LEFT JOIN juego_genero jg ON j.id = jg.juego_id
        LEFT JOIN generos g ON jg.genero_id = g.id
        WHERE g.nombre = ?
        GROUP BY j.id
        ORDER BY j.titulo
        """
        return self._ejecutar_consulta(query, (genero,))
    
    def buscar_por_titulo(self, titulo):
        """Busca juegos por título"""
        query = """
        SELECT 
            j.id, j.titulo, j.descripcion, j.anio_lanzamiento, 
            j.precio, j.imagen_ruta,
            GROUP_CONCAT(g.nombre, ', ') as generos
        FROM juegos j
        LEFT JOIN juego_genero jg ON j.id = jg.juego_id
        LEFT JOIN generos g ON jg.genero_id = g.id
        WHERE j.titulo LIKE ?
        GROUP BY j.id
        ORDER BY j.titulo
        """
        return self._ejecutar_consulta(query, ('%' + titulo + '%',))
    
    def obtener_por_anio(self, anio):
        """Obtiene juegos por año"""
        query = """
        SELECT 
            j.id, j.titulo, j.descripcion, j.anio_lanzamiento, 
            j.precio, j.imagen_ruta,
            GROUP_CONCAT(g.nombre, ', ') as generos
        FROM juegos j
        LEFT JOIN juego_genero jg ON j.id = jg.juego_id
        LEFT JOIN generos g ON jg.genero_id = g.id
        WHERE j.anio_lanzamiento = ?
        GROUP BY j.id
        ORDER BY j.titulo
        """
        return self._ejecutar_consulta(query, (anio,))
    
    def obtener_todos(self):
        """Obtiene todos los juegos"""
        query = """
        SELECT 
            j.id, j.titulo, j.descripcion, j.anio_lanzamiento, 
            j.precio, j.imagen_ruta,
            GROUP_CONCAT(g.nombre, ', ') as generos
        FROM juegos j
        LEFT JOIN juego_genero jg ON j.id = jg.juego_id
        LEFT JOIN generos g ON jg.genero_id = g.id
        GROUP BY j.id
        ORDER BY j.titulo
        """
        return self._ejecutar_consulta(query)
    
    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        try:
            self.cursor.close()
            self.conexion.close()
        except:
            pass