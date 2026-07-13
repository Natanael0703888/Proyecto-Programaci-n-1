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
        self.configurar_ui()
        self.cargar_juegos_iniciales()
    
    def configurar_ui(self):
        """Configura la interfaz de usuario"""
        # Colores PS3 mejorados
        self.COLORES = {
            'fondo': '#0a0a1a',
            'fondo_sec': '#141425',
            'azul_ps3': '#003087',
            'azul_medio': '#0055a4',
            'azul_claro': '#0078d4',
            'azul_brillante': '#0099ff',
            'gris': '#1a1a2e',
            'gris_claro': '#2a2a4a',
            'texto': '#ffffff',
            'texto_sec': '#8899bb',
            'texto_oscuro': '#667799',
            'verde': '#00cc66',
            'rojo': '#cc0033',
            'naranja': '#ff6600',
            'dorado': '#ffcc00',
            'sombra': '#00000030'
        }
        
        self.root.title("🎮 Catálogo de Juegos PS3")
        self.root.geometry("900x600")
        self.root.minsize(600, 500)
        self.root.config(bg=self.COLORES['fondo'])
        
        # Configurar grids
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Frame de búsqueda
        self._configurar_frame_busqueda()
        
        # Frame de menú
        self._configurar_frame_menu()
        
        # Frame con scrollbar
        self._configurar_frame_scroll()
        
        # Contador de resultados
        self._configurar_contador()
        
        # Bind para redimensionar
        self.root.bind("<Configure>", self._al_redimensionar_ventana)
    
    def _configurar_frame_busqueda(self):
        """Configura el frame de búsqueda con diseño mejorado"""
        frame_busqueda = tk.Frame(
            self.root,
            bg=self.COLORES['fondo_sec'],
            relief="flat",
            bd=0
        )
        frame_busqueda.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        frame_busqueda.grid_columnconfigure(0, weight=1)
        
        # Título del catálogo
        titulo = tk.Label(
            frame_busqueda,
            text="🎮 CATÁLOGO PS3",
            fg=self.COLORES['azul_brillante'],
            bg=self.COLORES['fondo_sec'],
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        titulo.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))
        
        # Subtítulo
        subtitulo = tk.Label(
            frame_busqueda,
            text="Explora nuestra colección de juegos",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['fondo_sec'],
            font=("Arial", 10),
            anchor="w"
        )
        subtitulo.grid(row=1, column=0, columnspan=3, sticky="w", pady=(0, 10))
        
        # Campo de búsqueda
        self.campo_busqueda = tk.Entry(
            frame_busqueda,
            width=50,
            font=("Arial", 12),
            bg="#1a1a2e",
            fg="white",
            insertbackground="white",
            relief="flat",
            bd=2,
            highlightbackground=self.COLORES['azul_medio'],
            highlightcolor=self.COLORES['azul_brillante'],
            highlightthickness=1
        )
        self.campo_busqueda.grid(row=2, column=0, padx=(0, 5), sticky="ew")
        self.campo_busqueda.bind("<Return>", lambda e: self.buscar_por_titulo())
        
        # Botón Buscar con icono
        btn_buscar = self._crear_boton(
            frame_busqueda,
            text="🔍 Buscar",
            command=self.buscar_por_titulo,
            color=self.COLORES['azul_claro'],
            color_hover=self.COLORES['azul_brillante']
        )
        btn_buscar.grid(row=2, column=1, padx=5)
        
        # Botón Limpiar
        btn_limpiar = self._crear_boton(
            frame_busqueda,
            text="✕",
            command=self.limpiar_busqueda,
            color=self.COLORES['gris_claro'],
            color_hover=self.COLORES['texto_sec'],
            ancho=3
        )
        btn_limpiar.grid(row=2, column=2, padx=(5, 0))
    
    def _configurar_frame_menu(self):
        """Configura el frame del menú con diseño mejorado"""
        frame_menu = tk.Frame(
            self.root,
            bg=self.COLORES['fondo_sec'],
            relief="flat",
            bd=0
        )
        frame_menu.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        
        # Contenedor izquierdo (filtros)
        frame_izquierda = tk.Frame(frame_menu, bg=self.COLORES['fondo_sec'])
        frame_izquierda.pack(side=tk.LEFT, fill="x", expand=True)
        
        # Botón Inicio
        btn_inicio = self._crear_boton(
            frame_izquierda,
            text="🏠 Inicio",
            command=self.ir_a_inicio,
            color=self.COLORES['azul_ps3'],
            color_hover=self.COLORES['azul_claro']
        )
        btn_inicio.pack(side=tk.LEFT, padx=2)
        
        # Separador
        tk.Frame(frame_izquierda, bg=self.COLORES['gris_claro'], width=1, height=30).pack(side=tk.LEFT, padx=10)
        
        # Etiqueta Género
        tk.Label(
            frame_izquierda,
            text="🎯 Género:",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['fondo_sec'],
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(5, 5))
        
        # Géneros
        generos = self.comunicacion.obtener_generos()
        self.variable_genero = tk.StringVar(self.root)
        self.variable_genero.set(generos[0] if generos else "Todos")
        
        self.menu_genero = ttk.OptionMenu(
            frame_izquierda,
            self.variable_genero,
            *generos,
            command=self.cargar_por_genero
        )
        self.menu_genero.pack(side=tk.LEFT, padx=5)
        
        # Estilo para OptionMenu
        style = ttk.Style()
        style.configure("TMenubutton", background="#1a1a2e", foreground="white")
        
        # Etiqueta Año
        tk.Label(
            frame_izquierda,
            text="📅 Año:",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['fondo_sec'],
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=(15, 5))
        
        # Años
        años = self.comunicacion.obtener_años_disponibles()
        self.variable_anio = tk.StringVar(self.root)
        self.variable_anio.set(años[0] if años else "2020")
        self.menu_anio = ttk.OptionMenu(frame_izquierda, self.variable_anio, *años)
        self.menu_anio.pack(side=tk.LEFT, padx=5)
        
        # Botón Buscar por Año
        btn_buscar_anio = self._crear_boton(
            frame_izquierda,
            text="📅 Filtrar",
            command=self.buscar_por_anio,
            color=self.COLORES['naranja'],
            color_hover="#ff8800"
        )
        btn_buscar_anio.pack(side=tk.LEFT, padx=5)
        
        # Contenedor derecho (acciones)
        frame_derecha = tk.Frame(frame_menu, bg=self.COLORES['fondo_sec'])
        frame_derecha.pack(side=tk.RIGHT)
        
        # Botón Salir
        btn_salir = self._crear_boton(
            frame_derecha,
            text="✕ Salir",
            command=self.salir,
            color=self.COLORES['rojo'],
            color_hover="#ff0044"
        )
        btn_salir.pack(side=tk.LEFT, padx=2)
    
    def _configurar_frame_scroll(self):
        """Configura el frame con scrollbar mejorado"""
        self.frame_contenedor = tk.Frame(
            self.root,
            bg=self.COLORES['fondo'],
            relief="flat",
            bd=0
        )
        self.frame_contenedor.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        self.frame_contenedor.grid_rowconfigure(0, weight=1)
        self.frame_contenedor.grid_columnconfigure(0, weight=1)
        
        # Canvas con fondo
        self.lienzo = tk.Canvas(
            self.frame_contenedor,
            bg=self.COLORES['fondo'],
            highlightthickness=0,
            relief="flat"
        )
        self.lienzo.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar estilizada
        self.scrollbar = ttk.Scrollbar(
            self.frame_contenedor,
            orient="vertical",
            command=self.lienzo.yview
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.lienzo.configure(yscrollcommand=self.scrollbar.set)
        
        # Frame interior
        self.frame_juegos = tk.Frame(self.lienzo, bg=self.COLORES['fondo'])
        self.ventana_lienzo = self.lienzo.create_window(
            (0, 0),
            window=self.frame_juegos,
            anchor="nw"
        )
        
        # Bindings
        self.frame_juegos.bind("<Configure>", self._al_configurar_frame)
        self.lienzo.bind("<Configure>", self._al_configurar_lienzo)
        self._vincular_rueda_mouse()
    
    def _configurar_contador(self):
        """Configura el contador de resultados"""
        self.etiqueta_contador = tk.Label(
            self.root,
            text="",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['fondo'],
            font=("Arial", 9)
        )
        self.etiqueta_contador.grid(row=3, column=0, sticky="se", padx=30, pady=(0, 10))
    
    def _crear_boton(self, padre, text, command, color, color_hover=None, ancho=None):
        """Crea un botón con estilo moderno"""
        color_hover = color_hover or color
    
        btn = tk.Button(
            padre,
            text=text,  # <--- Ahora usa 'text' en lugar de 'texto'
            command=command,  # <--- Ahora usa 'command' en lugar de 'comando'
            bg=color,
            fg=self.COLORES['texto'],
            font=("Arial", 9, "bold"),
            padx=12,
            pady=6,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=color_hover,
            activeforeground=self.COLORES['texto'],
            width=ancho
        )
    
    # Efecto hover
        def al_entrar(e):
            btn.config(bg=color_hover)
    
        def al_salir(e):
            btn.config(bg=color)
    
        btn.bind("<Enter>", al_entrar)
        btn.bind("<Leave>", al_salir)
    
        return btn
    
    def _vincular_rueda_mouse(self):
        """Habilita el scroll con la rueda del mouse"""
        def al_rueda_mouse(event):
            self.lienzo.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def al_rueda_mouse_linux(event):
            if event.num == 4:
                self.lienzo.yview_scroll(-1, "units")
            elif event.num == 5:
                self.lienzo.yview_scroll(1, "units")
        
        self.lienzo.bind("<MouseWheel>", al_rueda_mouse)
        self.frame_juegos.bind("<MouseWheel>", al_rueda_mouse)
        self.lienzo.bind("<Button-4>", al_rueda_mouse_linux)
        self.lienzo.bind("<Button-5>", al_rueda_mouse_linux)
        self.frame_juegos.bind("<Button-4>", al_rueda_mouse_linux)
        self.frame_juegos.bind("<Button-5>", al_rueda_mouse_linux)
    
    def _al_configurar_frame(self, event):
        self.lienzo.configure(scrollregion=self.lienzo.bbox("all"))
    
    def _al_configurar_lienzo(self, event):
        self.lienzo.itemconfig(self.ventana_lienzo, width=event.width)
        if self.juegos_actuales:
            self.mostrar_juegos(self.juegos_actuales)
    
    def _al_redimensionar_ventana(self, event):
        if event.widget == self.root and self.juegos_actuales:
            self.root.after(100, lambda: self.mostrar_juegos(self.juegos_actuales))
    
    def _crear_tarjeta(self, juego, fila, columna, padding):
        """Crea una tarjeta con diseño mejorado"""
        tarjeta = tk.Frame(
            self.frame_juegos,
            bg=self.COLORES['gris_claro'],
            relief="flat",
            bd=0,
            highlightbackground=self.COLORES['azul_medio'],
            highlightthickness=1
        )
        tarjeta.grid(
            row=fila,
            column=columna,
            padx=padding//2,
            pady=padding//2,
            sticky="nsew"
        )
        
        # Efecto hover en tarjeta
        def al_entrar(e):
            tarjeta.config(bg=self.COLORES['azul_medio'])
            for widget in tarjeta.winfo_children():
                if isinstance(widget, tk.Label):
                    if widget.cget('text') not in ["📅", "🎮"]:
                        widget.config(bg=self.COLORES['azul_medio'])
                elif isinstance(widget, tk.Frame):
                    widget.config(bg=self.COLORES['azul_medio'])
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.config(bg=self.COLORES['azul_medio'])
        
        def al_salir(e):
            tarjeta.config(bg=self.COLORES['gris_claro'])
            for widget in tarjeta.winfo_children():
                if isinstance(widget, tk.Label):
                    if widget.cget('text') not in ["📅", "🎮"]:
                        widget.config(bg=self.COLORES['gris_claro'])
                elif isinstance(widget, tk.Frame):
                    widget.config(bg=self.COLORES['gris_claro'])
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Label):
                            child.config(bg=self.COLORES['gris_claro'])
        
        tarjeta.bind("<Enter>", al_entrar)
        tarjeta.bind("<Leave>", al_salir)
        
        # Título
        tk.Label(
            tarjeta,
            text=juego.titulo_corto,
            font=("Arial", 10, "bold"),
            fg=self.COLORES['texto'],
            bg=self.COLORES['gris_claro'],
            wraplength=150
        ).pack(pady=(8, 2))
        
        # Año
        tk.Label(
            tarjeta,
            text=f"📅 {juego.anio or 'N/A'}",
            font=("Arial", 9),
            fg=self.COLORES['azul_brillante'],
            bg=self.COLORES['gris_claro']
        ).pack()
        
        # Imagen
        self._mostrar_imagen_tarjeta(tarjeta, juego)
        
        # Botón detalles mejorado
        btn = tk.Button(
            tarjeta,
            text="📖 Ver Detalles",
            command=lambda j=juego: self.abrir_detalles(j),
            bg=self.COLORES['azul_claro'],
            fg=self.COLORES['texto'],
            font=("Arial", 8, "bold"),
            padx=10,
            pady=3,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=self.COLORES['azul_brillante'],
            activeforeground=self.COLORES['texto']
        )
        btn.pack(pady=(5, 8))
    
    def _mostrar_imagen_tarjeta(self, tarjeta, juego):
        """Muestra la imagen en la tarjeta con marco"""
        frame_imagen = tk.Frame(tarjeta, bg=self.COLORES['gris_claro'])
        frame_imagen.pack(padx=10, pady=5)
        
        if juego.imagen and os.path.exists(juego.imagen):
            try:
                imagen = Image.open(juego.imagen)
                imagen = imagen.resize((100, 100), Image.Resampling.LANCZOS)
                imagen_tk = ImageTk.PhotoImage(imagen)
                lbl = tk.Label(frame_imagen, image=imagen_tk, bg=self.COLORES['gris_claro'])
                lbl.image = imagen_tk
                lbl.pack()
                return
            except:
                pass
        
        # Placeholder mejorado
        tk.Label(
            frame_imagen,
            text="🎮",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['gris_claro'],
            font=("Arial", 40)
        ).pack(padx=20, pady=20)
    
    def mostrar_juegos(self, juegos):
        """Muestra los juegos con contador"""
        self.juegos_actuales = juegos
        
        # Actualizar contador
        if juegos:
            self.etiqueta_contador.config(text=f"🎮 {len(juegos)} juegos encontrados")
        else:
            self.etiqueta_contador.config(text="📭 No se encontraron juegos")
        
        # Limpiar frame
        for widget in self.frame_juegos.winfo_children():
            widget.destroy()
        
        if not juegos:
            self._mostrar_mensaje_vacio()
            return
        
        # Calcular tarjetas por fila
        ancho_tarjeta = 180
        padding = 10
        ancho_lienzo = max(400, self.lienzo.winfo_width())
        tarjetas_por_fila = max(1, min(6, (ancho_lienzo - padding) // (ancho_tarjeta + padding)))
        
        # Configurar columnas
        for col in range(tarjetas_por_fila):
            self.frame_juegos.grid_columnconfigure(col, weight=1)
        
        # Crear tarjetas
        for i, juego in enumerate(juegos):
            fila = i // tarjetas_por_fila
            columna = i % tarjetas_por_fila
            self._crear_tarjeta(juego, fila, columna, padding)
        
        # Actualizar canvas
        self.frame_juegos.update_idletasks()
        self.lienzo.configure(scrollregion=self.lienzo.bbox("all"))
    
    def _mostrar_mensaje_vacio(self):
        """Muestra mensaje cuando no hay juegos"""
        frame = tk.Frame(self.frame_juegos, bg=self.COLORES['fondo'])
        frame.pack(expand=True, fill="both")
        
        tk.Label(
            frame,
            text="🎮",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['fondo'],
            font=("Arial", 60)
        ).pack(pady=(50, 10))
        
        tk.Label(
            frame,
            text="No hay juegos disponibles",
            font=("Arial", 16),
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['fondo']
        ).pack()
        
        tk.Label(
            frame,
            text="Prueba con otro filtro o búsqueda",
            font=("Arial", 11),
            fg=self.COLORES['texto_oscuro'],
            bg=self.COLORES['fondo']
        ).pack()
    
    # ============ MÉTODOS DE CONSULTA ============
    
    def cargar_juegos_iniciales(self):
        """Carga los juegos iniciales - TODOS los juegos"""
        # Establecer el género por defecto a "Acción"
        generos = self.comunicacion.obtener_generos()
        if generos:
            if "Acción" in generos:
                self.variable_genero.set("Acción")
            else:
                self.variable_genero.set(generos[0])
        
        # Establecer el año por defecto
        años = self.comunicacion.obtener_años_disponibles()
        if años:
            self.variable_anio.set(años[0])
        
        # Cargar todos los juegos
        juegos = self.comunicacion.obtener_todos()
        self.mostrar_juegos(juegos)
    
    def cargar_por_genero(self, *args):
        """Carga juegos por género"""
        genero = self.variable_genero.get()
        juegos = self.comunicacion.obtener_juegos_por_genero(genero)
        self.mostrar_juegos(juegos)
    
    def buscar_por_titulo(self):
        """Busca juegos por título"""
        titulo = self.campo_busqueda.get().strip()
        if not titulo:
            # Si no hay texto, recargar con el género actual
            self.cargar_por_genero()
            return
        juegos = self.comunicacion.buscar_por_titulo(titulo)
        self.mostrar_juegos(juegos)
    
    def buscar_por_anio(self):
        """Busca juegos por año"""
        anio = self.variable_anio.get()
        juegos = self.comunicacion.obtener_por_anio(anio)
        self.mostrar_juegos(juegos)
    
    def ir_a_inicio(self):
        """Vuelve al inicio - Muestra TODOS los juegos"""
        # Limpiar búsqueda
        self.campo_busqueda.delete(0, tk.END)
        
        # Restablecer el género a "Acción" o al primero de la lista
        generos = self.comunicacion.obtener_generos()
        if generos:
            if "Acción" in generos:
                self.variable_genero.set("Acción")
            else:
                self.variable_genero.set(generos[0])
        
        # Restablecer el año al primero
        años = self.comunicacion.obtener_años_disponibles()
        if años:
            self.variable_anio.set(años[0])
        
        # Cargar todos los juegos
        juegos = self.comunicacion.obtener_todos()
        self.mostrar_juegos(juegos)
    
    def limpiar_busqueda(self):
        """Limpia el campo de búsqueda y recarga el género actual"""
        self.campo_busqueda.delete(0, tk.END)
        # Recargar con el género actual seleccionado
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