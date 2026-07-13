import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import os

class VentanaDetalles:
    """Ventana emergente con detalles del juego"""
    
    def __init__(self, parent, juego):
        self.parent = parent
        self.juego = juego
        self.ventana = Toplevel(parent)
        self._setup_colores()
        self.setup_ui()
    
    def _setup_colores(self):
        """Define los colores de la ventana"""
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
            'verde': '#00cc66',
            'dorado': '#ffcc00',
            'naranja': '#ff6600'
        }
    
    def setup_ui(self):
        """Configura la ventana de detalles"""
        self.ventana.title(f"🎮 {self.juego.titulo}")
        self.ventana.geometry("800x400")
        self.ventana.minsize(600, 500)
        self.ventana.config(bg=self.COLORES['fondo'])
        
        self.parent.withdraw()
        
        # Contenedor principal
        contenedor = tk.Frame(
            self.ventana,
            bg=self.COLORES['fondo_sec'],
            relief="flat",
            bd=0
        )
        contenedor.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Botón atrás
        self._crear_boton_atras(contenedor)
        
        # Contenido
        contenido = tk.Frame(contenedor, bg=self.COLORES['fondo_sec'])
        contenido.pack(fill="both", expand=True, pady=10)
        
        # Frame de imagen (izquierda)
        frame_img = tk.Frame(contenido, bg=self.COLORES['fondo_sec'])
        frame_img.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 20))
        
        self._mostrar_imagen(frame_img)
        
        # Frame de detalles (derecha)
        frame_detalles = tk.Frame(contenido, bg=self.COLORES['fondo_sec'])
        frame_detalles.pack(side=tk.RIGHT, fill="both", expand=True)
        
        self._mostrar_detalles(frame_detalles)
    
    def _crear_boton_atras(self, parent):
        """Crea el botón de regreso"""
        btn_frame = tk.Frame(parent, bg=self.COLORES['fondo_sec'])
        btn_frame.pack(fill="x")
        
        btn = tk.Button(
            btn_frame,
            text="← Volver al catálogo",
            command=self.cerrar,
            bg=self.COLORES['azul_ps3'],
            fg=self.COLORES['texto'],
            font=("Arial", 10, "bold"),
            padx=15,
            pady=8,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground=self.COLORES['azul_claro'],
            activeforeground=self.COLORES['texto']
        )
        btn.pack(side=tk.LEFT)
        
        # Efecto hover
        def on_enter(e):
            btn.config(bg=self.COLORES['azul_claro'])
        
        def on_leave(e):
            btn.config(bg=self.COLORES['azul_ps3'])
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    
    def _mostrar_imagen(self, parent):
        """Muestra la imagen del juego con marco"""
        marco = tk.Frame(
            parent,
            bg=self.COLORES['gris'],
            relief="flat",
            bd=0,
            highlightbackground=self.COLORES['azul_medio'],
            highlightthickness=2
        )
        marco.pack(fill="both", expand=True, pady=20)
        
        if self.juego.imagen and os.path.exists(self.juego.imagen):
            try:
                imagen = Image.open(self.juego.imagen)
                imagen = imagen.resize((300, 300), Image.Resampling.LANCZOS)
                imagen_tk = ImageTk.PhotoImage(imagen)
                lbl = tk.Label(marco, image=imagen_tk, bg=self.COLORES['gris'])
                lbl.image = imagen_tk
                lbl.pack(expand=True)
                return
            except:
                pass
        
        # Placeholder mejorado
        tk.Label(
            marco,
            text="🎮",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['gris'],
            font=("Arial", 100)
        ).pack(expand=True)
    
    def _mostrar_detalles(self, parent):
        """Muestra los detalles del juego"""
        # Título
        tk.Label(
            parent,
            text=self.juego.titulo,
            fg=self.COLORES['azul_brillante'],
            bg=self.COLORES['fondo_sec'],
            font=("Arial", 20, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(0, 5))
        
        # Línea decorativa
        tk.Frame(parent, bg=self.COLORES['azul_claro'], height=2).pack(fill="x", pady=5)
        
        # Descripción
        tk.Label(
            parent,
            text="📝 Descripción",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['fondo_sec'],
            font=("Arial", 12, "bold"),
            anchor="w"
        ).pack(fill="x", pady=(10, 5))
        
        desc_frame = tk.Frame(
            parent,
            bg=self.COLORES['gris'],
            relief="flat",
            bd=0,
            highlightbackground=self.COLORES['azul_medio'],
            highlightthickness=1
        )
        desc_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        desc_texto = tk.Text(
            desc_frame,
            fg=self.COLORES['texto'],
            bg=self.COLORES['gris'],
            font=("Arial", 11),
            wrap="word",
            height=4,
            bd=0,
            relief="flat",
            padx=10,
            pady=10
        )
        desc_texto.insert("1.0", self.juego.descripcion or "No disponible")
        desc_texto.config(state=tk.DISABLED)
        desc_texto.pack(fill="both", expand=True)
        
        # Línea decorativa
        tk.Frame(parent, bg=self.COLORES['azul_claro'], height=1).pack(fill="x", pady=5)
        
        # Datos del juego
        datos = [
            ("🎯 Géneros: ", self.juego.generos or "No disponible"),
            ("📅 Año: ", str(self.juego.anio or "No disponible")),
            ("💰 Precio: ", self.juego.precio_formateado)
        ]
        
        # Frame para datos
        datos_frame = tk.Frame(parent, bg=self.COLORES['fondo_sec'])
        datos_frame.pack(fill="x", pady=10)
        
        for i, (label, valor) in enumerate(datos):
            # Fila
            fila = tk.Frame(datos_frame, bg=self.COLORES['fondo_sec'])
            fila.pack(fill="x", pady=3)
            
            # Etiqueta
            tk.Label(
                fila,
                text=label,
                fg=self.COLORES['texto_sec'],
                bg=self.COLORES['fondo_sec'],
                font=("Arial", 11, "bold"),
                width=15,
                anchor="w"
            ).pack(side=tk.LEFT)
            
            # Valor
            color_valor = self.COLORES['texto']
            if "Precio" in label and "USD" in str(valor):
                color_valor = self.COLORES['verde']
            elif "Año" in label and valor != "No disponible":
                color_valor = self.COLORES['dorado']
            
            tk.Label(
                fila,
                text=valor,
                fg=color_valor,
                bg=self.COLORES['fondo_sec'],
                font=("Arial", 11),
                anchor="w"
            ).pack(side=tk.LEFT)
    
    def cerrar(self):
        """Cierra la ventana y vuelve al menú principal"""
        self.parent.deiconify()
        self.ventana.destroy()