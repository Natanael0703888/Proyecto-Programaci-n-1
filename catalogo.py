# catalogo.py - Versión simple con grid y actualización al redimensionar

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
        self.root.geometry("800x500")
        self.root.minsize(400, 400)
        self.root.config(bg="#1D0A85")
        
        # Configurar grids principales
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Frame de búsqueda
        self.setup_search_frame()
        
        # Frame de menú
        self.setup_menu_frame()
        
        # Frame con scrollbar
        self.setup_scrollable_frame()
        
        # Cargar juegos iniciales
        self.cargar_juegos_por_genero()
        
        # Bind para redimensionar
        self.root.bind("<Configure>", self._on_window_resize)
    
    def setup_search_frame(self):
        """Configura el frame de búsqueda"""
        search_frame = tk.Frame(self.root, bg="#464545")
        search_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_entry = ttk.Entry(search_frame, width=50, font=("Arial", 12))
        self.search_entry.grid(row=0, column=0, padx=5, sticky="ew")
        
        btn_buscar = ttk.Button(search_frame, text="🔍 Buscar", command=self.buscar_juegos_por_titulo)
        btn_buscar.grid(row=0, column=1, padx=5)
    
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
        
        # Años
        años = self.comunicacion.obtener_años_disponibles()
        self.anio_var = tk.StringVar(self.root)
        self.anio_var.set(años[0] if años else "2020")
        self.anio_menu = ttk.OptionMenu(menu_frame, self.anio_var, *años)
        self.anio_menu.pack(side=tk.LEFT, padx=5)
        
        btn_buscar_anio = ttk.Button(menu_frame, text="📅 Buscar por Año", command=self.buscar_juegos_por_anio)
        btn_buscar_anio.pack(side=tk.LEFT, padx=5)
    
    def setup_scrollable_frame(self):
        """Configura el frame con scrollbar para los juegos"""
        # Frame contenedor principal
        self.container_frame = tk.Frame(self.root, bg="#121212")
        self.container_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)
        
        # Canvas para el scroll
        self.canvas = tk.Canvas(self.container_frame, bg="#121212", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar vertical
        self.scrollbar = ttk.Scrollbar(self.container_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Configurar canvas
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Frame interior donde se colocarán los juegos
        self.juegos_frame = tk.Frame(self.canvas, bg="#121212")
        
        # Crear ventana en el canvas
        self.canvas_window = self.canvas.create_window((0, 0), window=self.juegos_frame, anchor="nw")
        
        # Bind para redimensionar
        self.juegos_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        
        # Bind para el scroll con la rueda del mouse
        self._bind_mousewheel()
    
    def _on_frame_configure(self, event):
        """Actualizar el área de scroll cuando el frame cambia de tamaño"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Ajustar el ancho del frame interior al canvas"""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
        # Recalcular distribución si hay juegos cargados
        if hasattr(self, 'ultimos_juegos') and self.ultimos_juegos:
            self.mostrar_juegos(self.ultimos_juegos)
    
    def _on_window_resize(self, event):
        """Detectar redimensionamiento de la ventana principal"""
        if event.widget == self.root:
            # Actualizar el canvas después de un breve delay
            self.root.after(100, self._refresh_canvas)
    
    def _refresh_canvas(self):
        """Refrescar el canvas para que se ajuste al nuevo tamaño"""
        if hasattr(self, 'ultimos_juegos') and self.ultimos_juegos:
            self.mostrar_juegos(self.ultimos_juegos)
    
    def _bind_mousewheel(self):
        """Habilitar scroll con la rueda del mouse"""
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _on_mousewheel_linux(event):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")
        
        # Windows y macOS
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        self.juegos_frame.bind("<MouseWheel>", _on_mousewheel)
        
        # Linux
        self.canvas.bind("<Button-4>", _on_mousewheel_linux)
        self.canvas.bind("<Button-5>", _on_mousewheel_linux)
        self.juegos_frame.bind("<Button-4>", _on_mousewheel_linux)
        self.juegos_frame.bind("<Button-5>", _on_mousewheel_linux)
    
    def mostrar_juegos(self, juegos):
        """Método unificado para mostrar juegos en la interfaz"""
        # Guardar los juegos actuales
        self.ultimos_juegos = juegos
        
        # Limpiar frame
        for widget in self.juegos_frame.winfo_children():
            widget.destroy()
        
        if not juegos:
            tk.Label(self.juegos_frame, text="📭 No hay juegos disponibles.", 
                    font=("Arial", 14), fg="#888888", bg="#121212").pack(expand=True, pady=50)
            return
        
        # Calcular cuántas tarjetas caben por fila
        ANCHO_TARJETA = 170
        PADDING = 8
        
        # Obtener ancho del canvas
        ancho_canvas = self.canvas.winfo_width()
        if ancho_canvas <= 1:
            ancho_canvas = 800
        
        # Calcular tarjetas por fila (mínimo 1, máximo 6)
        tarjetas_por_fila = max(1, min(6, (ancho_canvas - PADDING) // (ANCHO_TARJETA + PADDING)))
        
        # Configurar columnas
        for col in range(tarjetas_por_fila):
            self.juegos_frame.grid_columnconfigure(col, weight=1)
        
        # Agregar las tarjetas
        for i, juego in enumerate(juegos):
            fila = i // tarjetas_por_fila
            columna = i % tarjetas_por_fila
            
            juego_frame = tk.Frame(
                self.juegos_frame, 
                bg="#1F1F1F", 
                relief="ridge", 
                bd=2
            )
            juego_frame.grid(
                row=fila, 
                column=columna, 
                padx=PADDING//2, 
                pady=PADDING//2,
                sticky="nsew"
            )
            
            # Título
            titulo_texto = juego[1][:22] + "..." if len(juego[1]) > 22 else juego[1]
            titulo = tk.Label(
                juego_frame, 
                text=titulo_texto, 
                font=("Arial", 10, "bold"), 
                fg="#FFFFFF", 
                bg="#1F1F1F",
                wraplength=150
            )
            titulo.pack(pady=(5,0))
            
            # Año
            año_label = tk.Label(
                juego_frame, 
                text=f"📅 {juego[5] if juego[5] else 'N/A'}", 
                font=("Arial", 9), 
                fg="#88AAFF", 
                bg="#1F1F1F"
            )
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
                    self._mostrar_placeholder_juego(juego_frame)
            else:
                self._mostrar_placeholder_juego(juego_frame)
            
            # Botón detalles
            detalles_button = ttk.Button(
                juego_frame, 
                text="📖 Detalles", 
                command=lambda j=juego: self.mostrar_detalles_juego(j),
                width=14
            )
            detalles_button.pack(pady=5)
        
        # Actualizar el canvas
        self.juegos_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _mostrar_placeholder_juego(self, frame):
        """Muestra un placeholder cuando no hay imagen"""
        tk.Label(
            frame, 
            text="🎮", 
            fg="#444444", 
            bg="#1F1F1F", 
            font=("Arial", 36)
        ).pack(padx=10, pady=10)
    
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
        generos = self.comunicacion.obtener_generos()
        if generos:
            self.categoria_var.set(generos[0])
        self.cargar_juegos_por_genero()
    
    

    # catalogo.py - Solo la parte corregida en mostrar_detalles_juego

    def mostrar_detalles_juego(self, juego):
        """Muestra los detalles de un juego en una ventana emergente"""
        ventana = Toplevel(self.root)
        ventana.title(f"Detalles - {juego[1]}")
        ventana.geometry("800x600")
        ventana.minsize(500, 400)
        ventana.config(bg="#1A1A1A")
        
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
        contenedor.grid_columnconfigure(0, weight=0)
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
            except Exception as e:
                print(f"Error al cargar imagen: {e}")
                self._mostrar_placeholder_detalles(frame_img)
        else:
            self._mostrar_placeholder_detalles(frame_img)
        
        # Frame de detalles
        frame_detalles = tk.Frame(contenedor, bg="#1A1A1A", relief="sunken", bd=1)
        frame_detalles.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        frame_detalles.grid_columnconfigure(0, weight=1)
        
        # Título del juego
        titulo_label = tk.Label(
            frame_detalles, 
            text=f"🎮 {juego[1]}", 
            fg="#FFFFFF", 
            bg="#1A1A1A", 
            font=("Arial", 16, "bold"),
            anchor="w"
        )
        titulo_label.pack(fill="x", pady=(10, 5))
        
        # Línea separadora
        tk.Frame(frame_detalles, bg="#3A3A3A", height=2).pack(fill="x", pady=5)
        
        # Descripción
        desc_frame = tk.Frame(frame_detalles, bg="#1A1A1A")
        desc_frame.pack(fill="both", expand=True, pady=5)
        
        desc_label = tk.Label(
            desc_frame, 
            text="📝 Descripción:", 
            fg="#88AAFF", 
            bg="#1A1A1A", 
            font=("Arial", 11, "bold"),
            anchor="w"
        )
        desc_label.pack(fill="x")
        
        desc_texto = tk.Text(
            desc_frame, 
            fg="#FFFFFF", 
            bg="#1A1A1A", 
            font=("Arial", 11), 
            wrap="word", 
            height=5, 
            bd=0, 
            relief="flat"
        )
        desc_texto.insert("1.0", juego[2] if juego[2] else "No disponible")
        desc_texto.config(state=tk.DISABLED)
        desc_texto.pack(fill="both", expand=True, pady=(0, 10))
        
        # Línea separadora
        tk.Frame(frame_detalles, bg="#3A3A3A", height=2).pack(fill="x", pady=5)
        
        # Datos del juego
        datos_frame = tk.Frame(frame_detalles, bg="#1A1A1A")
        datos_frame.pack(fill="x", pady=5)
        
        # === CORRECCIÓN DEL PRECIO ===
        # Intentar convertir el precio a float, si falla mostrar "No disponible"
        try:
            precio = float(juego[6]) if juego[6] else None
            precio_texto = f"${precio:.2f}" if precio else "No disponible"
        except (ValueError, TypeError):
            precio_texto = "No disponible"
        
        info_juego = [
            ("🎯 Género", juego[3] if juego[3] else "No disponible"),
            ("🖥️ Plataforma", juego[4] if juego[4] else "No disponible"),
            ("📅 Año", juego[5] if juego[5] else "No disponible"),
            ("💰 Precio", precio_texto)
        ]
        
        for i, (label, valor) in enumerate(info_juego):
            tk.Label(
                datos_frame, 
                text=f"{label}:", 
                fg="#88AAFF", 
                bg="#1A1A1A", 
                font=("Arial", 11, "bold"),
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=3, padx=(0, 10))
            
            tk.Label(
                datos_frame, 
                text=valor, 
                fg="#FFFFFF", 
                bg="#1A1A1A", 
                font=("Arial", 11),
                anchor="w"
            ).grid(row=i, column=1, sticky="w", pady=3)
    
    def _mostrar_placeholder_detalles(self, frame):
        """Muestra un placeholder cuando no hay imagen en detalles"""
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