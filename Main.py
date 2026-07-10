import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from catalogo import CatalogoJuegos

def main():
    """Función principal"""
    root = tk.Tk()
    app = CatalogoJuegos(root)
    
    try:
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            app.comunicacion.cerrar_conexion()
        except:
            pass

if __name__ == "__main__":
    main()