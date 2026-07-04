# catalogo.py - Refactorizado

import tkinter as tk
from tkinter import Toplevel, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import io
from conexion import Comunicacion

class CatalogoJuegos:
    def __init__(self, root):
        self.root = root
        self.comunicacion = Comunicacion()
        self.setup_ui()
        
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        self.root.title("Catálogo de Juegos PS3")
        self.root.geometry("900x700")
        self.root.minsize(500, 400)
        self.root.config(bg="#121212")
        
        # Configurar grids
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Frame de búsqueda
        self.setup_search_frame()
        
        # Frame de menú
        self.setup_menu_frame()
        
        # Frame de juegos
        self.juegos_frame = tk.Frame(self.root, bg="#121212")
        self.juegos_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.juegos_frame.grid_columnconfigure(0, weight=1)
        
        # Cargar juegos iniciales
        self.cargar_juegos_por_genero()
    
    def setup_search_frame(self):
        """Configura el frame de búsqueda"""
        search_frame = tk.Frame(self.root, bg="#1A1A1A")
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        self.search_entry = ttk.Entry(search_frame, width=50, font=("Arial", 12))
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        btn_buscar = ttk.Button(search_frame, text="🔍 Buscar", command=self.buscar_juegos_por_titulo)
        btn_buscar.pack(side=tk.LEFT, padx=5)
    
    def setup_menu_frame(self):
        """Configura el frame del menú"""
        menu_frame = tk.Frame(self.root, bg="#121212")
        menu_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        # Botón Inicio
        btn_inicio = ttk.Button(menu_frame, text="🏠 Inicio", command=self.ir_a_inicio)
        btn_inicio.pack(side=tk.LEFT, padx=5)
        
        # Géneros
        generos = self.comunicacion.obtener_generos()
        self.categoria_var = tk.StringVar(self.root)
        self.categoria_var.set(generos[0] if generos else "Todos")
        self.categoria_menu = ttk.OptionMenu(menu_frame, self.categoria_var, *generos, command=self.cargar_juegos_por_genero)
        self.categoria_menu.pack(side=tk.LEFT, padx=5)
        
        # Años - Ahora con años reales disponibles
        años = self.comunicacion.obtener_años_disponibles()
        self.anio_var = tk.StringVar(self.root)
        self.anio_var.set(años[0] if años else "2020")
        self.anio_menu = ttk.OptionMenu(menu_frame, self.anio_var, *años)
        self.anio_menu.pack(side=tk.LEFT, padx=5)
        
        btn_buscar_anio = ttk.Button(menu_frame, text="📅 Buscar por Año", command=self.buscar_juegos_por_anio)
        btn_buscar_anio.pack(side=tk.LEFT, padx=5)
    
    def mostrar_juegos(self, juegos):
        """Método unificado para mostrar juegos en la interfaz"""
        # Limpiar frame
        for widget in self.juegos_frame.winfo_children():
            widget.destroy()
        
        if not juegos:
            tk.Label(self.juegos_frame, text="No hay juegos disponibles.", 
                    font=("Arial", 14), fg="#888888", bg="#121212").pack(expand=True)
            return
        
        # Configurar columnas
        columnas = 4
        for col in range(columnas):
            self.juegos_frame.grid_columnconfigure(col, weight=1)
        
        for i, juego in enumerate(juegos):
            juego_frame = tk.Frame(self.juegos_frame, bg="#1F1F1F", relief="ridge", bd=2)
            juego_frame.grid(row=i // columnas, column=i % columnas, padx=8, pady=8, sticky="nsew")
            
            # Título
            titulo = tk.Label(juego_frame, text=f"{juego[1][:30]}", 
                            font=("Arial", 11, "bold"), fg="#FFFFFF", bg="#1F1F1F")
            titulo.pack(pady=(5,0))
            
            # Año
            año_label = tk.Label(juego_frame, text=f"📅 {juego[5]}", 
                               font=("Arial", 9), fg="#88AAFF", bg="#1F1F1F")
            año_label.pack()
            
            # Imagen
            if juego[7]:
                try:
                    imagen = Image.open(io.BytesIO(juego[7]))
                    imagen = imagen.resize((100, 100), Image.Resampling.LANCZOS)
                    imagen_tk = ImageTk.PhotoImage(imagen)
                    img_label = tk.Label(juego_frame, image=imagen_tk, bg="#1F1F1F")
                    img_label.image = imagen_tk
                    img_label.pack(padx=10, pady=5)
                except Exception as e:
                    print(f"Error al cargar imagen: {e}")
            
            # Botón detalles
            detalles_button = ttk.Button(juego_frame, text="📖 Detalles", 
                                       command=lambda j=juego: self.mostrar_detalles_juego(j))
            detalles_button.pack(pady=5)
    
    def cargar_juegos_por_genero(self, *args):
        """Carga juegos filtrados por género"""
        genero = self.categoria_var.get()
        juegos = self.comunicacion.obtener_juegos_por_genero(genero)
        self.mostrar_juegos(juegos)
    
    def buscar_juegos_por_titulo(self):
        """Busca juegos por título"""
        titulo = self.search_entry.get().strip()
        if not titulo:
            self.cargar_juegos_por_genero()
            return
        juegos = self.comunicacion.buscar_juego_por_titulo(titulo)
        self.mostrar_juegos(juegos)
    
    def buscar_juegos_por_anio(self):
        """Busca juegos por año"""
        anio = self.anio_var.get()
        juegos = self.comunicacion.obtener_juegos_por_anio(anio)
        self.mostrar_juegos(juegos)
    
    def ir_a_inicio(self):
        """Vuelve a la vista inicial"""
        self.search_entry.delete(0, tk.END)
        self.categoria_var.set(self.comunicacion.obtener_generos()[0])
        self.cargar_juegos_por_genero()
    
    def mostrar_detalles_juego(self, juego):
        """Muestra los detalles de un juego en una ventana emergente"""
        ventana = Toplevel(self.root)
        ventana.title(f"Detalles - {juego[1]}")
        ventana.geometry("800x600")
        ventana.minsize(500, 400)
        ventana.config(bg="#1A1A1A")
        
        # Prevenir cerrar la ventana principal
        self.root.withdraw()
        
        def cerrar():
            self.root.deiconify()
            ventana.destroy()
        
        # Botón atrás
        btn_atras = ttk.Button(ventana, text="← Atrás", command=cerrar)
        btn_atras.pack(anchor="nw", pady=10, padx=10)
        
        # Contenedor principal
        contenedor = tk.Frame(ventana, bg="#2C2C2C", relief="groove", bd=3)
        contenedor.pack(pady=10, padx=10, fill="both", expand=True)
        contenedor.grid_columnconfigure(1, weight=1)
        contenedor.grid_rowconfigure(0, weight=1)
        
        # Frame de imagen
        frame_img = tk.Frame(contenedor, bg="#2C2C2C")
        frame_img.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        
        if juego[7]:
            try:
                imagen = Image.open(io.BytesIO(juego[7]))
                imagen = imagen.resize((280, 280), Image.Resampling.LANCZOS)
                imagen_tk = ImageTk.PhotoImage(imagen)
                lbl_img = tk.Label(frame_img, image=imagen_tk, bg="#2C2C2C")
                lbl_img.image = imagen_tk
                lbl_img.pack()
            except:
                self._mostrar_placeholder_imagen(frame_img)
        else:
            self._mostrar_placeholder_imagen(frame_img)
        
        # Frame de detalles
        frame_detalles = tk.Frame(contenedor, bg="#1A1A1A")
        frame_detalles.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Datos del juego
        datos = [
            ("🎮 Título", juego[1]),
            ("📝 Descripción", juego[2]),
            ("🎯 Género", juego[3]),
            ("🖥️ Plataforma", juego[4]),
            ("📅 Año", juego[5]),
            ("💰 Precio", f"${juego[6]:.2f}" if juego[6] else "No disponible")
        ]
        
        for i, (label, valor) in enumerate(datos):
            if label == "📝 Descripción":
                desc = tk.Text(frame_detalles, fg="#FFFFFF", bg="#1A1A1A", 
                             font=("Arial", 11), wrap="word", height=5, bd=0, relief="flat")
                desc.insert(tk.END, valor or "No disponible")
                desc.config(state=tk.DISABLED)
                desc.pack(fill="x", pady=5)
            else:
                tk.Label(frame_detalles, text=f"{label}: {valor or 'No disponible'}", 
                        fg="#FFFFFF", bg="#1A1A1A", font=("Arial", 12), anchor="w").pack(fill="x", pady=3)
    
    def _mostrar_placeholder_imagen(self, frame):
        """Muestra un placeholder cuando no hay imagen"""
        tk.Label(frame, text="🎮", fg="#666666", bg="#2C2C2C", 
                font=("Arial", 80)).pack()

# Punto de entrada
if __name__ == "__main__":
    root = tk.Tk()
    app = CatalogoJuegos(root)
    try:
        root.mainloop()
    finally:
        app.comunicacion.cerrar_conexion()