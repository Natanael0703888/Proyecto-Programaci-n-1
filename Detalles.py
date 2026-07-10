# Detalles.py
"""Ventana de detalles del juego"""

import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import os

class VentanaDetalles:
    """Ventana emergente con detalles del juego"""
    
    # Colores PS3
    AZUL = "#003087"
    AZUL_MEDIO = "#0055a4"
    AZUL_CLARO = "#0070cc"
    GRIS = "#1a1a1a"
    GRIS_CLARO = "#2a2a2a"
    TEXTO = "#ffffff"
    TEXTO_SEC = "#999999"
    
    def __init__(self, parent, juego):
        self.parent = parent
        self.juego = juego
        self.ventana = Toplevel(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la ventana de detalles"""
        self.ventana.title(f"Detalles - {self.juego.titulo}")
        self.ventana.geometry("800x600")
        self.ventana.minsize(500, 400)
        self.ventana.config(bg=self.AZUL)
        
        # Ocultar ventana principal
        self.parent.withdraw()
        
        # Botón atrás
        btn_atras = tk.Button(
            self.ventana,
            text="← Atrás",
            command=self.cerrar,
            bg=self.AZUL_CLARO,
            fg=self.TEXTO,
            font=("Arial", 10, "bold"),
            padx=10,
            relief="flat",
            activebackground=self.AZUL_MEDIO,
            activeforeground=self.TEXTO
        )
        btn_atras.pack(anchor="nw", pady=10, padx=10)
        
        # Contenedor principal
        contenedor = tk.Frame(
            self.ventana,
            bg=self.GRIS_CLARO,
            relief="groove",
            bd=3
        )
        contenedor.pack(pady=10, padx=10, fill="both", expand=True)
        contenedor.grid_columnconfigure(0, weight=0)
        contenedor.grid_columnconfigure(1, weight=1)
        contenedor.grid_rowconfigure(0, weight=1)
        
        # Frame de imagen
        self._mostrar_imagen(contenedor)
        
        # Frame de detalles
        self._mostrar_detalles(contenedor)
    
    def _mostrar_imagen(self, contenedor):
        """Muestra la imagen del juego"""
        frame_img = tk.Frame(contenedor, bg=self.GRIS_CLARO)
        frame_img.grid(row=0, column=0, padx=20, pady=20, sticky="n")
        
        if self.juego.imagen and os.path.exists(self.juego.imagen):
            try:
                imagen = Image.open(self.juego.imagen)
                imagen = imagen.resize((280, 280), Image.Resampling.LANCZOS)
                imagen_tk = ImageTk.PhotoImage(imagen)
                lbl = tk.Label(frame_img, image=imagen_tk, bg=self.GRIS_CLARO)
                lbl.image = imagen_tk
                lbl.pack()
                return
            except:
                pass
        
        # Placeholder
        tk.Label(
            frame_img,
            text="🎮",
            fg="#666666",
            bg=self.GRIS_CLARO,
            font=("Arial", 80)
        ).pack()
    
    def _mostrar_detalles(self, contenedor):
        """Muestra los detalles del juego"""
        frame = tk.Frame(
            contenedor,
            bg=self.GRIS,
            relief="sunken",
            bd=1
        )
        frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        frame.grid_columnconfigure(0, weight=0)  # Columna etiquetas
        frame.grid_columnconfigure(1, weight=1)  # Columna valores
        frame.grid_rowconfigure(3, weight=1)     # Fila de descripción
        
        # Título (ocupa 2 columnas)
        tk.Label(
            frame,
            text=f"🎮 {self.juego.titulo}",
            fg=self.TEXTO,
            bg=self.GRIS,
            font=("Arial", 16, "bold"),
            anchor="w"
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(10, 5), padx=10)
        
        # Separador
        tk.Frame(frame, bg=self.AZUL_CLARO, height=2).grid(row=1, column=0, columnspan=2, sticky="ew", pady=5, padx=10)
        
        # Descripción - Etiqueta
        tk.Label(
            frame,
            text="📝 Descripción:",
            fg=self.AZUL_CLARO,
            bg=self.GRIS,
            font=("Arial", 11, "bold"),
            anchor="w"
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 0), padx=10)
        
        # Descripción - Texto
        desc_texto = tk.Text(
            frame,
            fg=self.TEXTO,
            bg=self.GRIS,
            font=("Arial", 11),
            wrap="word",
            height=5,
            bd=0,
            relief="flat"
        )
        desc_texto.insert("1.0", self.juego.descripcion or "No disponible")
        desc_texto.config(state=tk.DISABLED)
        desc_texto.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(0, 10), padx=10)
        
        # Separador
        tk.Frame(frame, bg=self.AZUL_CLARO, height=2).grid(row=4, column=0, columnspan=2, sticky="ew", pady=5, padx=10)
        
        # Datos del juego
        datos = [
            ("🎯 Géneros", self.juego.generos or "No disponible"),
            ("📅 Año", self.juego.anio or "No disponible"),
            ("💰 Precio", self.juego.precio_formateado)
        ]
        
        for i, (label, valor) in enumerate(datos):
            # Etiqueta (columna 0)
            tk.Label(
                frame,
                text=f"{label}:",
                fg=self.AZUL_CLARO,
                bg=self.GRIS,
                font=("Arial", 11, "bold"),
                anchor="w"
            ).grid(row=i+5, column=0, sticky="w", pady=3, padx=(10, 5))
            
            # Valor (columna 1)
            tk.Label(
                frame,
                text=valor,
                fg=self.TEXTO,
                bg=self.GRIS,
                font=("Arial", 11),
                anchor="w"
            ).grid(row=i+5, column=1, sticky="w", pady=3, padx=(5, 10))
    
    def cerrar(self):
        """Cierra la ventana y vuelve al menú principal"""
        self.parent.deiconify()
        self.ventana.destroy()