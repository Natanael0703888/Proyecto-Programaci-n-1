import tkinter as tk
from tkinter import Toplevel, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import io
from conexion import Comunicacion

# Crear la instancia de la clase Comunicacion
comunicacion = Comunicacion()

# Función para cargar los juegos de acuerdo al género seleccionado
def cargar_juegos_por_genero(*args):
    genero_seleccionado = categoria_var.get()
    juegos = comunicacion.obtener_juegos_por_genero(genero_seleccionado)

    # Limpiar la interfaz antes de mostrar nuevos juegos
    for widget in juegos_frame.winfo_children():
        widget.destroy()

    if juegos:
        for i, juego in enumerate(juegos):
            juego_frame = tk.Frame(juegos_frame, bg="#1F1F1F")
            juego_frame.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky="nsew")

            titulo_juego = tk.Label(juego_frame, text=f"{juego[1]} ({juego[5]})", font=("Arial", 10), fg="#FFFFFF", bg="#1F1F1F")
            titulo_juego.pack()

            if juego[7]:
                try:
                    imagen_binaria = juego[7]
                    imagen = Image.open(io.BytesIO(imagen_binaria))
                    imagen = imagen.resize((80, 80), Image.Resampling.LANCZOS)
                    imagen_tk = ImageTk.PhotoImage(imagen)
                    img_label = tk.Label(juego_frame, image=imagen_tk, bg="#1F1F1F")
                    img_label.image = imagen_tk
                    img_label.pack(padx=10, pady=10)
                except Exception as e:
                    print(f"Error al cargar imagen: {e}")

            detalles_button = ttk.Button(juego_frame, text="Detalles", command=lambda juego=juego: mostrar_detalles_juego(juego), width=20)
            detalles_button.pack(pady=5)

        # Hacer que los juegos se distribuyan dinámicamente
        for col in range(4):
            juegos_frame.grid_columnconfigure(col, weight=1)
    else:
        tk.Label(juegos_frame, text="No hay juegos disponibles en este género.", font=("Arial", 10), fg="#FFFFFF", bg="#1F1F1F").pack()

# Función para buscar juegos por título
def buscar_juegos_por_titulo():
    titulo_busqueda = search_entry.get()
    juegos = comunicacion.buscar_juego_por_titulo(titulo_busqueda)

    # Limpiar la interfaz antes de mostrar nuevos juegos
    for widget in juegos_frame.winfo_children():
        widget.destroy()

    if juegos:
        for i, juego in enumerate(juegos):
            juego_frame = tk.Frame(juegos_frame, bg="#1F1F1F")
            juego_frame.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky="nsew")

            titulo_juego = tk.Label(juego_frame, text=f"{juego[1]} ({juego[5]})", font=("Arial", 10), fg="#FFFFFF", bg="#1F1F1F")
            titulo_juego.pack()

            if juego[7]:
                try:
                    imagen_binaria = juego[7]
                    imagen = Image.open(io.BytesIO(imagen_binaria))
                    imagen = imagen.resize((80, 80), Image.Resampling.LANCZOS)
                    imagen_tk = ImageTk.PhotoImage(imagen)
                    img_label = tk.Label(juego_frame, image=imagen_tk, bg="#1F1F1F")
                    img_label.image = imagen_tk
                    img_label.pack(padx=10, pady=10)
                except Exception as e:
                    print(f"Error al cargar imagen: {e}")

            detalles_button = ttk.Button(juego_frame, text="Detalles", command=lambda juego=juego: mostrar_detalles_juego(juego), width=20)
            detalles_button.pack(pady=5)

        # Hacer que los juegos se distribuyan dinámicamente
        for col in range(4):
            juegos_frame.grid_columnconfigure(col, weight=1)
    else:
        tk.Label(juegos_frame, text="No se encontraron juegos con ese título.", font=("Arial", 10), fg="#FFFFFF", bg="#1F1F1F").pack()

# Función para mostrar los detalles del juego seleccionado
def mostrar_detalles_juego(juego):
    ventana_detalles = Toplevel(root)
    ventana_detalles.title(f"Detalles de {juego[1]}")
    ventana_detalles.geometry("720x600")
    ventana_detalles.config(bg="#1A1A1A")
    ventana_detalles.minsize(500, 400)

    root.withdraw()

    def regresar():
        root.deiconify()
        ventana_detalles.destroy()

    btn_atras = ttk.Button(ventana_detalles, text="Atrás", command=regresar)
    btn_atras.pack(anchor="nw", pady=10, padx=10)

    marco_principal = tk.Frame(ventana_detalles, bg="#2C2C2C", relief="groove", bd=3)
    marco_principal.pack(pady=10, padx=10, fill="both", expand=True)

    frame_imagen = tk.Frame(marco_principal, bg="#2C2C2C")
    frame_imagen.grid(row=0, column=0, padx=20, pady=20, sticky="n")

    if juego[7]:
        try:
            imagen_binaria = juego[7]
            imagen = Image.open(io.BytesIO(imagen_binaria))
            imagen = imagen.resize((300, 300), Image.Resampling.LANCZOS)
            imagen_tk = ImageTk.PhotoImage(imagen)
            lbl_imagen = tk.Label(frame_imagen, image=imagen_tk, bg="#2C2C2C")
            lbl_imagen.image = imagen_tk
            lbl_imagen.pack()
        except Exception as e:
            print(f"Error al cargar imagen: {e}")
    else:
        
        tk.Label(frame_imagen, text="🎮 Sin imagen disponible", fg="#FFFFFF", bg="#2C2C2C", font=("Arial", 20)).pack()

    frame_detalles = tk.Frame(marco_principal, bg="#1A1A1A")
    frame_detalles.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def agregar_etiqueta(texto):
        lbl = tk.Label(frame_detalles, text=texto, fg="#FFFFFF", bg="#1A1A1A", font=("Arial", 12), anchor="w")
        lbl.pack(fill="x", pady=5)
        return lbl

    # Mostrar detalles del juego
    agregar_etiqueta(f"Título: {juego[1]}")
    #Cambio2
    # Descripción: Usamos un Text widget para que se ajuste al tamaño de la ventana
    descripcion_texto = tk.Text(frame_detalles, fg="#FFFFFF", bg="#1A1A1A", font=("Arial", 12), wrap="word", height=6, width=40, bd=0)
    descripcion_texto.insert(tk.END, juego[2] if juego[2] else '❓ No disponible')
    descripcion_texto.config(state=tk.DISABLED)  # Hacer el Text widget solo lectura
    descripcion_texto.pack(fill="x", pady=5)

    agregar_etiqueta(f"Género: {juego[3] if juego[3] else '🎮 No disponible'}")
    agregar_etiqueta(f"Plataforma: {juego[4] if juego[4] else '🖥️ No disponible'}")
    agregar_etiqueta(f"Año: {juego[5] if juego[5] else '❓ No disponible'}")

    marco_principal.grid_columnconfigure(1, weight=1)
    marco_principal.grid_rowconfigure(0, weight=1)

    ventana_detalles.mainloop()
    
#Cambio1
def buscar_juegos_por_anio():
    anio_buscado = anio_var.get()
    juegos = comunicacion.obtener_juegos_por_anio(anio_buscado)

    # Limpiar la interfaz antes de mostrar nuevos juegos
    for widget in juegos_frame.winfo_children():
        widget.destroy()

    if juegos:
        for i, juego in enumerate(juegos):
            juego_frame = tk.Frame(juegos_frame, bg="#1F1F1F")
            juego_frame.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky="nsew")

            titulo_juego = tk.Label(juego_frame, text=f"{juego[1]} ({juego[5]})", font=("Arial", 10), fg="#FFFFFF", bg="#1F1F1F")
            titulo_juego.pack()

            if juego[7]:
                try:
                    imagen_binaria = juego[7]
                    imagen = Image.open(io.BytesIO(imagen_binaria))
                    imagen = imagen.resize((80, 80), Image.Resampling.LANCZOS)
                    imagen_tk = ImageTk.PhotoImage(imagen)
                    img_label = tk.Label(juego_frame, image=imagen_tk, bg="#1F1F1F")
                    img_label.image = imagen_tk
                    img_label.pack(padx=10, pady=10)
                except Exception as e:
                    print(f"Error al cargar imagen: {e}")

            detalles_button = ttk.Button(juego_frame, text="Detalles", command=lambda juego=juego: mostrar_detalles_juego(juego), width=20)
            detalles_button.pack(pady=5)

        # Hacer que los juegos se distribuyan dinámicamente
        for col in range(4):
            juegos_frame.grid_columnconfigure(col, weight=1)
    else:
        tk.Label(juegos_frame, text="No se encontraron juegos para ese año.", font=("Arial", 10), fg="#FFFFFF", bg="#1F1F1F").pack()

#Cambio1

def ir_a_inicio():
    search_entry.delete(0, tk.END)
    cargar_juegos_por_genero()

root = tk.Tk()
root.title("Catálogo de Juegos PS3")
root.geometry("800x600")
root.minsize(500, 400)
root.config(bg="#121212")

search_frame = tk.Frame(root, bg="#1A1A1A")
search_frame.pack(fill="x", pady=10, padx=10)

search_entry = ttk.Entry(search_frame, width=50, font=("Arial", 12))
search_entry.pack(side=tk.LEFT, padx=5)

btn_buscar = ttk.Button(search_frame, text="Buscar", command=buscar_juegos_por_titulo)
btn_buscar.pack(side=tk.LEFT, padx=5)

menu_frame = tk.Frame(root, bg="#121212")
menu_frame.pack(fill="x", pady=10, padx=10)

btn_inicio = ttk.Button(menu_frame, text="Inicio", command=ir_a_inicio)
btn_inicio.pack(side=tk.LEFT, padx=10)

generos = comunicacion.obtener_generos()
categoria_var = tk.StringVar(root)
categoria_var.set(generos[0])
categoria_menu = ttk.OptionMenu(menu_frame, categoria_var, *generos, command=cargar_juegos_por_genero)
categoria_menu.pack(side=tk.LEFT, padx=10)

#Cambio2
# Agregar la opción para seleccionar el año
anio_var = tk.StringVar(root)
anio_var.set("2020")  # Establecer un valor por defecto
anio_menu = ttk.OptionMenu(menu_frame, anio_var, *[str(anio) for anio in range(2004, 2014)])
anio_menu.pack(side=tk.LEFT, padx=10)

# Botón para buscar juegos por año
btn_buscar_anio = ttk.Button(menu_frame, text="Buscar por Año", command=buscar_juegos_por_anio)
btn_buscar_anio.pack(side=tk.LEFT, padx=10)
#Cambio2

juegos_frame = tk.Frame(root, bg="#121212")
juegos_frame.pack(pady=10, fill="both", expand=True)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
comunicacion.cerrar_conexion()
