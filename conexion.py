# conexion.py - Adaptado para la nueva estructura de base de datos

import sqlite3
import os

class Comunicacion:
    def __init__(self):
        # Usamos el mismo nombre de archivo para mantener compatibilidad
        ruta_db = os.path.join(os.path.dirname(__file__), 'juegos_ps3.db')
        if not os.path.exists(ruta_db):
            raise FileNotFoundError(f"Base de datos no encontrada: {ruta_db}")
        self.conexion = sqlite3.connect(ruta_db)
        self.cursor = self.conexion.cursor()
    
    # ============ MÉTODOS DE CONSULTA ============
    
    def obtener_todos_los_juegos(self):
        """Obtiene todos los juegos con sus géneros"""
        query = """
        SELECT 
            j.id,
            j.titulo,
            j.descripcion,
            j.anio_lanzamiento,
            j.precio,
            j.imagen_ruta,
            GROUP_CONCAT(g.nombre, ', ') as generos
        FROM juegos j
        LEFT JOIN juego_genero jg ON j.id = jg.juego_id
        LEFT JOIN generos g ON jg.genero_id = g.id
        GROUP BY j.id
        ORDER BY j.titulo
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def obtener_generos(self):
        """Obtiene la lista de géneros disponibles"""
        self.cursor.execute("SELECT nombre FROM generos ORDER BY nombre")
        return [g[0] for g in self.cursor.fetchall()]
    
    def obtener_años_disponibles(self):
        """Obtiene los años disponibles en la base de datos"""
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
            j.id,
            j.titulo,
            j.descripcion,
            j.anio_lanzamiento,
            j.precio,
            j.imagen_ruta,
            GROUP_CONCAT(g.nombre, ', ') as generos
        FROM juegos j
        LEFT JOIN juego_genero jg ON j.id = jg.juego_id
        LEFT JOIN generos g ON jg.genero_id = g.id
        WHERE g.nombre = ?
        GROUP BY j.id
        ORDER BY j.titulo
        """
        self.cursor.execute(query, (genero,))
        return self.cursor.fetchall()
    
    def buscar_juego_por_titulo(self, titulo):
        """Busca juegos por título (búsqueda parcial)"""
        query = """
        SELECT 
            j.id,
            j.titulo,
            j.descripcion,
            j.anio_lanzamiento,
            j.precio,
            j.imagen_ruta,
            GROUP_CONCAT(g.nombre, ', ') as generos
        FROM juegos j
        LEFT JOIN juego_genero jg ON j.id = jg.juego_id
        LEFT JOIN generos g ON jg.genero_id = g.id
        WHERE j.titulo LIKE ?
        GROUP BY j.id
        ORDER BY j.titulo
        """
        self.cursor.execute(query, ('%' + titulo + '%',))
        return self.cursor.fetchall()
    
    def obtener_juegos_por_anio(self, anio):
        """Obtiene juegos filtrados por año"""
        query = """
        SELECT 
            j.id,
            j.titulo,
            j.descripcion,
            j.anio_lanzamiento,
            j.precio,
            j.imagen_ruta,
            GROUP_CONCAT(g.nombre, ', ') as generos
        FROM juegos j
        LEFT JOIN juego_genero jg ON j.id = jg.juego_id
        LEFT JOIN generos g ON jg.genero_id = g.id
        WHERE j.anio_lanzamiento = ?
        GROUP BY j.id
        ORDER BY j.titulo
        """
        self.cursor.execute(query, (anio,))
        return self.cursor.fetchall()
    
    def obtener_juego_por_id(self, juego_id):
        """Obtiene un juego específico por su ID"""
        query = """
        SELECT 
            j.id,
            j.titulo,
            j.descripcion,
            j.anio_lanzamiento,
            j.precio,
            j.imagen_ruta,
            GROUP_CONCAT(g.nombre, ', ') as generos
        FROM juegos j
        LEFT JOIN juego_genero jg ON j.id = jg.juego_id
        LEFT JOIN generos g ON jg.genero_id = g.id
        WHERE j.id = ?
        GROUP BY j.id
        """
        self.cursor.execute(query, (juego_id,))
        return self.cursor.fetchone()
    
    # ============ MÉTODOS DE MODIFICACIÓN ============
    
    def agregar_juego(self, titulo, descripcion, anio, precio, generos, imagen_ruta=None):
        """Agrega un nuevo juego a la base de datos"""
        try:
            # 1. Insertar el juego
            self.cursor.execute("""
                INSERT INTO juegos (titulo, descripcion, anio_lanzamiento, precio, imagen_ruta)
                VALUES (?, ?, ?, ?, ?)
            """, (titulo, descripcion, anio, precio, imagen_ruta))
            juego_id = self.cursor.lastrowid
            
            # 2. Relacionar con géneros
            for genero_nombre in generos:
                # Obtener o crear el género
                self.cursor.execute("SELECT id FROM generos WHERE nombre = ?", (genero_nombre,))
                resultado = self.cursor.fetchone()
                if resultado:
                    genero_id = resultado[0]
                else:
                    self.cursor.execute("INSERT INTO generos (nombre) VALUES (?)", (genero_nombre,))
                    genero_id = self.cursor.lastrowid
                
                # Crear la relación
                self.cursor.execute("""
                    INSERT INTO juego_genero (juego_id, genero_id)
                    VALUES (?, ?)
                """, (juego_id, genero_id))
            
            self.conexion.commit()
            return juego_id
        except Exception as e:
            print(f"Error al agregar juego: {e}")
            self.conexion.rollback()
            return None
    
    def actualizar_juego(self, juego_id, titulo, descripcion, anio, precio, generos, imagen_ruta=None):
        """Actualiza un juego existente"""
        try:
            # 1. Actualizar la información del juego
            self.cursor.execute("""
                UPDATE juegos 
                SET titulo = ?, 
                    descripcion = ?, 
                    anio_lanzamiento = ?, 
                    precio = ?,
                    imagen_ruta = COALESCE(?, imagen_ruta)
                WHERE id = ?
            """, (titulo, descripcion, anio, precio, imagen_ruta, juego_id))
            
            # 2. Eliminar relaciones de géneros antiguas
            self.cursor.execute("DELETE FROM juego_genero WHERE juego_id = ?", (juego_id,))
            
            # 3. Insertar las nuevas relaciones
            for genero_nombre in generos:
                self.cursor.execute("SELECT id FROM generos WHERE nombre = ?", (genero_nombre,))
                resultado = self.cursor.fetchone()
                if resultado:
                    genero_id = resultado[0]
                else:
                    self.cursor.execute("INSERT INTO generos (nombre) VALUES (?)", (genero_nombre,))
                    genero_id = self.cursor.lastrowid
                
                self.cursor.execute("""
                    INSERT INTO juego_genero (juego_id, genero_id)
                    VALUES (?, ?)
                """, (juego_id, genero_id))
            
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar juego: {e}")
            self.conexion.rollback()
            return False
    
    def actualizar_precio(self, juego_id, nuevo_precio):
        """Actualiza el precio de un juego"""
        try:
            self.cursor.execute("""
                UPDATE juegos 
                SET precio = ? 
                WHERE id = ?
            """, (nuevo_precio, juego_id))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar precio: {e}")
            return False
    
    def actualizar_imagen(self, juego_id, ruta_imagen):
        """Actualiza la imagen de un juego (ruta al archivo)"""
        try:
            self.cursor.execute("""
                UPDATE juegos 
                SET imagen_ruta = ? 
                WHERE id = ?
            """, (ruta_imagen, juego_id))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar imagen: {e}")
            return False
    
    def eliminar_juego(self, juego_id):
        """Elimina un juego (ON DELETE CASCADE elimina sus relaciones)"""
        try:
            self.cursor.execute("DELETE FROM juegos WHERE id = ?", (juego_id,))
            self.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar juego: {e}")
            return False
    
    # ============ MÉTODOS DE ESTADÍSTICAS ============
    
    def contar_juegos_por_genero(self):
        """Cuenta cuántos juegos hay por género"""
        query = """
        SELECT 
            g.nombre,
            COUNT(jg.juego_id) as cantidad
        FROM generos g
        LEFT JOIN juego_genero jg ON g.id = jg.genero_id
        GROUP BY g.id
        ORDER BY cantidad DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def obtener_precio_promedio_por_anio(self):
        """Obtiene el precio promedio de juegos por año"""
        query = """
        SELECT 
            anio_lanzamiento,
            ROUND(AVG(precio), 2) as precio_promedio,
            COUNT(*) as cantidad
        FROM juegos
        WHERE anio_lanzamiento IS NOT NULL AND precio IS NOT NULL
        GROUP BY anio_lanzamiento
        ORDER BY anio_lanzamiento DESC
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    # ============ MÉTODO DE CIERRE ============
    
    def cerrar_conexion(self):
        """Cierra la conexión a la base de datos"""
        try:
            self.cursor.close()
            self.conexion.close()
        except:
            pass