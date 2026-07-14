import tkinter as tk
from tkinter import Toplevel, messagebox
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
            'naranja': '#ff6600',
            'rojo': '#cc0033'
        }
    
    def setup_ui(self):
        """Configura la ventana de detalles"""
        self.ventana.title(f"🎮 {self.juego.titulo}")
        self.ventana.geometry("600x500")  # Tamaño más pequeño
        self.ventana.minsize(600, 450)    # Mínimo más pequeño
        self.ventana.config(bg=self.COLORES['fondo'])
        
        self.parent.withdraw()
        
        # Contenedor principal
        contenedor = tk.Frame(
            self.ventana,
            bg=self.COLORES['fondo_sec'],
            relief="flat",
            bd=0
        )
        contenedor.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Botón atrás
        self._crear_boton_atras(contenedor)
        
        # Contenido
        contenido = tk.Frame(contenedor, bg=self.COLORES['fondo_sec'])
        contenido.pack(fill="both", expand=True, pady=8)
        
        # Frame de imagen (izquierda)
        frame_img = tk.Frame(contenido, bg=self.COLORES['fondo_sec'])
        frame_img.pack(side=tk.LEFT, fill="both", expand=True, padx=(0, 15))
        
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
            text="← Volver",
            command=self.cerrar,
            bg=self.COLORES['azul_ps3'],
            fg=self.COLORES['texto'],
            font=("Arial", 9, "bold"),
            padx=12,
            pady=5,
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
        marco.pack(fill="both", expand=True, pady=10)
        
        if self.juego.imagen and os.path.exists(self.juego.imagen):
            try:
                imagen = Image.open(self.juego.imagen)
                imagen = imagen.resize((200, 200), Image.Resampling.LANCZOS)  # Imagen más pequeña
                imagen_tk = ImageTk.PhotoImage(imagen)
                lbl = tk.Label(marco, image=imagen_tk, bg=self.COLORES['gris'])
                lbl.image = imagen_tk
                lbl.pack(expand=True)
                return
            except:
                pass
        
        # Placeholder más pequeño
        tk.Label(
            marco,
            text="🎮",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['gris'],
            font=("Arial", 70)  # Más pequeño
        ).pack(expand=True)
    
    def _mostrar_detalles(self, parent):
        """Muestra los detalles del juego"""
        # Título
        tk.Label(
            parent,
            text=self.juego.titulo,
            fg=self.COLORES['azul_brillante'],
            bg=self.COLORES['fondo_sec'],
            font=("Arial", 16, "bold"),  # Más pequeño
            anchor="w"
        ).pack(fill="x", pady=(0, 3))
        
        # Línea decorativa
        tk.Frame(parent, bg=self.COLORES['azul_claro'], height=2).pack(fill="x", pady=3)
        
        # Descripción
        tk.Label(
            parent,
            text="📝 Descripción",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['fondo_sec'],
            font=("Arial", 10, "bold"),  # Más pequeño
            anchor="w"
        ).pack(fill="x", pady=(5, 3))
        
        desc_frame = tk.Frame(
            parent,
            bg=self.COLORES['gris'],
            relief="flat",
            bd=0,
            highlightbackground=self.COLORES['azul_medio'],
            highlightthickness=1
        )
        desc_frame.pack(fill="both", expand=True, pady=(0, 5))
        
        desc_texto = tk.Text(
            desc_frame,
            fg=self.COLORES['texto'],
            bg=self.COLORES['gris'],
            font=("Arial", 10),  # Más pequeño
            wrap="word",
            height=3,  # Menos altura
            bd=0,
            relief="flat",
            padx=8,
            pady=8
        )
        desc_texto.insert("1.0", self.juego.descripcion or "No disponible")
        desc_texto.config(state=tk.DISABLED)
        desc_texto.pack(fill="both", expand=True)
        
        # Línea decorativa
        tk.Frame(parent, bg=self.COLORES['azul_claro'], height=1).pack(fill="x", pady=3)
        
        # Datos del juego
        datos_frame = tk.Frame(parent, bg=self.COLORES['fondo_sec'])
        datos_frame.pack(fill="x", pady=5)
        
        # Configurar columnas
        datos_frame.grid_columnconfigure(0, weight=0, minsize=100)
        datos_frame.grid_columnconfigure(1, weight=1)
        
        datos = [
            ("🎯 Géneros", self.juego.generos or "No disponible"),
            ("📅 Año", str(self.juego.anio or "No disponible")),
            ("💰 Precio", self.juego.precio_formateado)
        ]
        
        for i, (label, valor) in enumerate(datos):
            # Etiqueta
            tk.Label(
                datos_frame,
                text=label,
                fg=self.COLORES['texto_sec'],
                bg=self.COLORES['fondo_sec'],
                font=("Arial", 10, "bold"),  # Más pequeño
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=2, padx=(0, 8))
            
            # Valor
            color_valor = self.COLORES['texto']
            if "Precio" in label and "USD" in str(valor):
                color_valor = self.COLORES['verde']
            elif "Año" in label and valor != "No disponible":
                color_valor = self.COLORES['dorado']
            
            tk.Label(
                datos_frame,
                text=valor,
                fg=color_valor,
                bg=self.COLORES['fondo_sec'],
                font=("Arial", 10),  # Más pequeño
                anchor="w"
            ).grid(row=i, column=1, sticky="w", pady=2)
        
        # Botón Agregar a Favoritos
        self._crear_boton_favoritos(parent)
    
    def _crear_boton_favoritos(self, parent):
        """Crea el botón para agregar a favoritos"""
        frame_boton = tk.Frame(parent, bg=self.COLORES['fondo_sec'])
        frame_boton.pack(fill="x", pady=(8, 0))
        
        btn_favoritos = tk.Button(
            frame_boton,
            text="⭐ Agregar a Favoritos",
            command=self.agregar_favoritos,
            bg=self.COLORES['dorado'],
            fg="#1a1a2e",
            font=("Arial", 10, "bold"),  # Más pequeño
            padx=15,
            pady=7,
            relief="flat",
            bd=0,
            cursor="hand2",
            activebackground="#ffdd44",
            activeforeground="#1a1a2e"
        )
        btn_favoritos.pack(fill="x")
        
        # Efecto hover
        def on_enter(e):
            btn_favoritos.config(bg="#ffdd44")
        
        def on_leave(e):
            btn_favoritos.config(bg=self.COLORES['dorado'])
        
        btn_favoritos.bind("<Enter>", on_enter)
        btn_favoritos.bind("<Leave>", on_leave)
        
        # Texto informativo más pequeño
        tk.Label(
            frame_boton,
            text="💡 Función disponible solo con suscripción",
            fg=self.COLORES['texto_sec'],
            bg=self.COLORES['fondo_sec'],
            font=("Arial", 7),  # Más pequeño
            anchor="center"
        ).pack(fill="x", pady=(3, 0))
    
    def agregar_favoritos(self):
        """Muestra mensaje de que la función requiere suscripción"""
        messagebox.showinfo(
            "⭐ Agregar a Favoritos",
            "Próximamente disponible con una suscripción de $1.99\n\n"
            "💳 Beneficios de la suscripción:\n"
            "• Guardar juegos en favoritos\n"
            "• Lista personalizada\n"
            "• Recomendaciones exclusivas\n"
            "• Acceso a contenido premium\n\n"
            "🔜 ¡Muy pronto disponible!"
        )
    
    def cerrar(self):
        """Cierra la ventana y vuelve al menú principal"""
        self.parent.deiconify()
        self.ventana.destroy()