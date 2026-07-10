# catalogo.py
"""Catálogo de juegos PS3 - Ventana principal"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os

from conexion import Comunicacion
from Detalles import VentanaDetalles
from Juego_model import Juego

class CatalogoJuegos:
    def __init__(self, root):
        self.root = root
        self.comunicacion = Comunicacion()
        self.juegos_actuales = []
        self.setup_ui()
        self.cargar_juegos_iniciales()
    
    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Colores PS3
        self.AZUL = "#003087"
        self.AZUL_MEDIO = "#0055a4"
        self.AZUL_CLARO = "#0070cc"
        self.GRIS = "#1a1a1a"
        self.GRIS_CLARO = "#2a2a2a"
        self.TEXTO = "#ffffff"
        self.TEXTO_SEC = "#999999"
        self.ROJO = "#cc0000"
        
        self.root.title("Catálogo de Juegos PS3")
        self.root.geometry("800x500")
        self.root.minsize(400, 400)
        self.root.config(bg=self.AZUL)
        
        # Configurar grids
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Frame de búsqueda
        self._setup_search_frame()
        
        # Frame de menú
        self._setup_menu_frame()
        
        # Frame con scrollbar
        self._setup_scrollable_frame()
        
        # Bind para redimensionar
        self.root.bind("<Configure>", self._on_window_resize)
    
    def _setup_search_frame(self):
        """Configura el frame de búsqueda"""
        search_frame = tk.Frame(self.root, bg=self.GRIS)
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ttk.Entry(search_frame, width=50, font=("Arial", 12))
        self.search_entry.grid(row=0, column=0, padx=5, sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self.buscar_por_titulo())
        
        btn_buscar = tk.Button(
            search_frame,
            text="🔍 Buscar",
            command=self.buscar_por_titulo,
            bg=self.AZUL_CLARO,
            fg=self.TEXTO,
            font=("Arial", 10, "bold"),
            padx=10,
            relief="flat",
            activebackground=self.AZUL_MEDIO,
            activeforeground=self.TEXTO
        )
        btn_buscar.grid(row=0, column=1, padx=5)
    
    def _setup_menu_frame(self):
        """Configura el frame del menú"""
        menu_frame = tk.Frame(self.root, bg=self.GRIS)
        menu_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        # Botón Inicio
        btn_inicio = tk.Button(
            menu_frame,
            text="🏠 Inicio",
            command=self.ir_a_inicio,
            bg=self.AZUL_CLARO,
            fg=self.TEXTO,
            font=("Arial", 10, "bold"),
            padx=10,
            relief="flat",
            activebackground=self.AZUL_MEDIO,
            activeforeground=self.TEXTO
        )
        btn_inicio.pack(side=tk.LEFT, padx=5)
        
        # Géneros
        generos = self.comunicacion.obtener_generos()
        self.categoria_var = tk.StringVar(self.root)
        self.categoria_var.set(generos[0] if generos else "Todos")
        self.categoria_menu = ttk.OptionMenu(
            menu_frame,
            self.categoria_var,
            *generos,
            command=self.cargar_por_genero
        )
        self.categoria_menu.pack(side=tk.LEFT, padx=5)
        
        # Años
        años = self.comunicacion.obtener_años_disponibles()
        self.anio_var = tk.StringVar(self.root)
        self.anio_var.set(años[0] if años else "2020")
        self.anio_menu = ttk.OptionMenu(menu_frame, self.anio_var, *años)
        self.anio_menu.pack(side=tk.LEFT, padx=5)
        
        btn_buscar_anio = tk.Button(
            menu_frame,
            text="📅 Buscar por Año",
            command=self.buscar_por_anio,
            bg=self.AZUL_CLARO,
            fg=self.TEXTO,
            font=("Arial", 10, "bold"),
            padx=10,
            relief="flat",
            activebackground=self.AZUL_MEDIO,
            activeforeground=self.TEXTO
        )
        btn_buscar_anio.pack(side=tk.LEFT, padx=5)
        
        # Botón Salir
        btn_salir = tk.Button(
            menu_frame,
            text="❌ Salir",
            command=self.salir,
            bg=self.ROJO,
            fg=self.TEXTO,
            font=("Arial", 10, "bold"),
            padx=15,
            relief="flat",
            activebackground="#990000",
            activeforeground=self.TEXTO
        )
        btn_salir.pack(side=tk.RIGHT, padx=5)
    
    def _setup_scrollable_frame(self):
        """Configura el frame con scrollbar"""
        # Frame contenedor
        self.container_frame = tk.Frame(self.root, bg=self.GRIS)
        self.container_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas
        self.canvas = tk.Canvas(
            self.container_frame,
            bg=self.GRIS,
            highlightthickness=0
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.container_frame,
            orient="vertical",
            command=self.canvas.yview
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Frame interior
        self.juegos_frame = tk.Frame(self.canvas, bg=self.GRIS)
        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.juegos_frame,
            anchor="nw"
        )
        
        # Bindings
        self.juegos_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self._bind_mousewheel()
    
    def _bind_mousewheel(self):
        """Habilita el scroll con la rueda del mouse"""
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def on_mousewheel_linux(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
        
        self.canvas.bind("<MouseWheel>", on_mousewheel)
        self.juegos_frame.bind("<MouseWheel>", on_mousewheel)
        self.canvas.bind("<Button-4>", on_mousewheel_linux)
        self.canvas.bind("<Button-5>", on_mousewheel_linux)
        self.juegos_frame.bind("<Button-4>", on_mousewheel_linux)
        self.juegos_frame.bind("<Button-5>", on_mousewheel_linux)
    
    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        if self.juegos_actuales:
            self.mostrar_juegos(self.juegos_actuales)
    
    def _on_window_resize(self, event):
        if event.widget == self.root and self.juegos_actuales:
            self.root.after(100, lambda: self.mostrar_juegos(self.juegos_actuales))
    
    # ============ MÉTODOS DE CARGA ============
    
    def cargar_juegos_iniciales(self):
        """Carga los juegos iniciales"""
        generos = self.comunicacion.obtener_generos()
        if generos:
            self.categoria_var.set(generos[0])
            self.cargar_por_genero()
    
    def mostrar_juegos(self, juegos):
        """Muestra los juegos en la interfaz"""
        self.juegos_actuales = juegos
        
        # Limpiar frame
        for widget in self.juegos_frame.winfo_children():
            widget.destroy()
        
        if not juegos:
            tk.Label(
                self.juegos_frame,
                text="📭 No hay juegos disponibles.",
                font=("Arial", 14),
                fg=self.TEXTO_SEC,
                bg=self.GRIS
            ).pack(expand=True, pady=50)
            return
        
        # Calcular tarjetas por fila
        ancho_tarjeta = 170
        padding = 8
        ancho_canvas = max(400, self.canvas.winfo_width())
        tarjetas_por_fila = max(1, min(6, (ancho_canvas - padding) // (ancho_tarjeta + padding)))
        
        # Configurar columnas
        for col in range(tarjetas_por_fila):
            self.juegos_frame.grid_columnconfigure(col, weight=1)
        
        # Crear tarjetas
        for i, juego in enumerate(juegos):
            fila = i // tarjetas_por_fila
            columna = i % tarjetas_por_fila
            
            self._crear_tarjeta(juego, fila, columna, padding)
        
        # Actualizar canvas
        self.juegos_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _crear_tarjeta(self, juego, fila, columna, padding):
        """Crea una tarjeta para un juego"""
        tarjeta = tk.Frame(
            self.juegos_frame,
            bg=self.GRIS_CLARO,
            relief="ridge",
            bd=2,
            highlightbackground=self.AZUL_MEDIO,
            highlightthickness=1
        )
        tarjeta.grid(
            row=fila,
            column=columna,
            padx=padding//2,
            pady=padding//2,
            sticky="nsew"
        )
        
        # Título
        tk.Label(
            tarjeta,
            text=juego.titulo_corto,
            font=("Arial", 10, "bold"),
            fg=self.TEXTO,
            bg=self.GRIS_CLARO,
            wraplength=150
        ).pack(pady=(5, 0))
        
        # Año
        tk.Label(
            tarjeta,
            text=f"📅 {juego.anio or 'N/A'}",
            font=("Arial", 9),
            fg=self.AZUL_CLARO,
            bg=self.GRIS_CLARO
        ).pack()
        
        # Imagen
        self._mostrar_imagen_tarjeta(tarjeta, juego)
        
        # Botón detalles
        btn = tk.Button(
            tarjeta,
            text="📖 Detalles",
            command=lambda j=juego: self.abrir_detalles(j),
            bg=self.AZUL_CLARO,
            fg=self.TEXTO,
            font=("Arial", 9, "bold"),
            padx=5,
            pady=2,
            relief="flat",
            activebackground=self.AZUL_MEDIO,
            activeforeground=self.TEXTO
        )
        btn.pack(pady=5)
    
    def _mostrar_imagen_tarjeta(self, tarjeta, juego):
        """Muestra la imagen en la tarjeta"""
        if juego.imagen and os.path.exists(juego.imagen):
            try:
                imagen = Image.open(juego.imagen)
                imagen = imagen.resize((100, 100), Image.Resampling.LANCZOS)
                imagen_tk = ImageTk.PhotoImage(imagen)
                lbl = tk.Label(tarjeta, image=imagen_tk, bg=self.GRIS_CLARO)
                lbl.image = imagen_tk
                lbl.pack(padx=10, pady=5)
                return
            except:
                pass
        
        # Placeholder
        tk.Label(
            tarjeta,
            text="🎮",
            fg="#444444",
            bg=self.GRIS_CLARO,
            font=("Arial", 36)
        ).pack(padx=10, pady=10)
    
    # ============ MÉTODOS DE CONSULTA ============
    
    def cargar_por_genero(self, *args):
        """Carga juegos por género"""
        genero = self.categoria_var.get()
        juegos = self.comunicacion.obtener_juegos_por_genero(genero)
        self.mostrar_juegos(juegos)
    
    def buscar_por_titulo(self):
        """Busca juegos por título"""
        titulo = self.search_entry.get().strip()
        if not titulo:
            self.cargar_por_genero()
            return
        juegos = self.comunicacion.buscar_por_titulo(titulo)
        self.mostrar_juegos(juegos)
    
    def buscar_por_anio(self):
        """Busca juegos por año"""
        anio = self.anio_var.get()
        juegos = self.comunicacion.obtener_por_anio(anio)
        self.mostrar_juegos(juegos)
    
    def ir_a_inicio(self):
        """Vuelve al inicio"""
        self.search_entry.delete(0, tk.END)
        generos = self.comunicacion.obtener_generos()
        if generos:
            self.categoria_var.set(generos[0])
        self.cargar_por_genero()
    
    def abrir_detalles(self, juego):
        """Abre la ventana de detalles"""
        VentanaDetalles(self.root, juego)
    
    def salir(self):
        """Sale de la aplicación"""
        if messagebox.askyesno("Salir", "¿Estás seguro de que quieres salir?"):
            try:
                self.comunicacion.cerrar_conexion()
            except:
                pass
            self.root.quit()
            self.root.destroy()