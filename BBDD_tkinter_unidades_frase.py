import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext

# Verificar instalación de Python 3.10 (esto usualmente no se hace desde un script de Python)
print("\n\t\t Comprobando que Python 3.10 está instalado.....")
os.system('winget install "Python.Python.3.10"')

# Inicializamos el diccionario vacío
db = {}
filename = "unidades_fraseologicas.txt"

# Cambiar a la carpeta de Descargas
ruta = os.getcwd()
pos = ruta.index('Users')
user_dir = ruta[:pos] + ruta[pos:ruta.index('\\', pos+6)+1]
downloads_dir = os.path.join(user_dir, 'Downloads')
os.chdir(downloads_dir)
ruta_completa = os.path.join(downloads_dir, filename)

# Leer db del archivo TXT
try:
    with open(ruta_completa, 'r', encoding='utf-8') as f:
        db = json.load(f)
except FileNotFoundError or Exception:  # añadi Exception en general por si acaso
    with open(ruta_completa, 'w+', encoding='utf-8') as f:
        json.dump({}, f)

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Base de Datos de Unidades Fraseológicas")

# Crear marco para el contenido
marco_contenido = tk.Frame(ventana)
marco_contenido.pack(padx=100, pady=100)

# Crear área de texto con scroll
area_texto = scrolledtext.ScrolledText(marco_contenido, width=80, height=20)
area_texto.pack()

# Función para actualizar el área de texto
def mostrar_db_entera():
    area_texto.config(state=tk.NORMAL)
    area_texto.delete(1.0, tk.END)
    for clave, valor in db.items():
        area_texto.insert(tk.END, f"Clave: {clave}\nValor: {valor}\n\n")
    area_texto.config(state=tk.DISABLED)

# Clase personalizada para el diálogo
class CustomSimpleDialog(simpledialog._QueryString):
    def __init__(self, parent, title, prompt):
        super().__init__(parent, title, prompt)

    def body(self, master):
        self.geometry("350x350")
        return super().body(master)

def ask_custom_string(title, prompt):
    return CustomSimpleDialog(ventana, title, prompt).result

# Funciones para las operaciones
def añadir():
    clave = ask_custom_string("Añadir", "Introduce la clave:").lower()
    valor = ask_custom_string("Añadir", "Introduce el valor:").lower()
    if clave in db:
        if type(db[clave]) is list and valor not in db[clave]:
            db[clave].append(valor)
        elif db[clave] == "" or db[clave] is None:
            db[clave] = valor
        elif db[clave] != valor:
            db[clave] = [db[clave], valor]
    else:
        db[clave] = valor
    mostrar_db_entera()

def buscar(en_claves=True, en_valores=False):
    palabra = ask_custom_string("Buscar", "Introduce la palabra a buscar:").lower()
    resultados = []
    for clave, valor in db.items():
        if en_claves and palabra in clave:
            resultados.append((clave, valor))
        if en_valores and palabra in str(valor):
            resultados.append((clave, valor))
    area_texto.config(state=tk.NORMAL)
    area_texto.delete(1.0, tk.END)
    for clave, valor in resultados:
        area_texto.insert(tk.END, f"Clave: {clave}\nValor: {valor}\n\n")
    area_texto.config(state=tk.DISABLED)

def borrar_pareja():
    clave = ask_custom_string("Borrar", "Introduce la clave de la pareja a borrar:").lower()
    if clave in db:
        del db[clave]
    else:
        messagebox.showerror("Error", "La clave no existe.")
    mostrar_db_entera()

def borrar_valor():
    clave = ask_custom_string("Borrar valor", "Introduce la clave del valor a borrar:").lower()
    if clave in db:
        db[clave] = ""
    else:
        messagebox.showerror("Error", "La clave no existe.")
    mostrar_db_entera()

def borrar_string_tupla():
    clave = ask_custom_string("Borrar string", "Introduce la clave de la pareja:").lower()
    string = ask_custom_string("Borrar string", "Introduce el string a borrar:").lower()
    if clave in db.keys() and (type(db[clave]) is list or type(db[clave]) is tuple) and string in db[clave]:
        db[clave].remove(string)
        if len(db[clave]) == 1:
            db[clave] = str(db[clave])
    else:
        messagebox.showerror("Error", "La clave no existe o el string no está en la lista.")
    mostrar_db_entera()

def salir():
    ver_exit = ask_custom_string("¿quieres ver la Base de datos antes de salir?", "Elige: y / n").lower()
    if ver_exit == 'y':
        mostrar_db_entera()
    elif ver_exit == 'n':
        pass
    else:
        while ver_exit not in ('y', 'n'):
            ver_exit = ask_custom_string("Ver BBDD completa", "Elige: y / n").lower()
    save_exit = ask_custom_string("¿quieres guardar los cambios antes de salir?", "Elige: y / n").lower()
    if save_exit == 'y':
        on_closing()
    elif save_exit == 'n':
        pass
    else:
        while save_exit not in ('y', 'n'):
            save_exit = ask_custom_string("Ver BBDD completa", "Elige: y / n").lower()
    ventana.destroy()

# Crear botones
boton_añadir = tk.Button(marco_contenido, text="Añadir", command=añadir)
boton_añadir.pack(side=tk.LEFT, padx=5, pady=5)

boton_buscar_clave = tk.Button(marco_contenido, text="Buscar en claves", command=lambda: buscar(en_claves=True, en_valores=False))
boton_buscar_clave.pack(side=tk.LEFT, padx=5, pady=5)

boton_buscar_valor = tk.Button(marco_contenido, text="Buscar en valores", command=lambda: buscar(en_claves=False, en_valores=True))
boton_buscar_valor.pack(side=tk.LEFT, padx=5, pady=5)

boton_borrar_pareja = tk.Button(marco_contenido, text="Borrar pareja", command=borrar_pareja)
boton_borrar_pareja.pack(side=tk.LEFT, padx=5, pady=5)

boton_borrar_valor = tk.Button(marco_contenido, text="Borrar valor", command=borrar_valor)
boton_borrar_valor.pack(side=tk.LEFT, padx=5, pady=5)

boton_borrar_string = tk.Button(marco_contenido, text="Borrar string", command=borrar_string_tupla)
boton_borrar_string.pack(side=tk.LEFT, padx=5, pady=5)

boton_salir = tk.Button(marco_contenido, text="Salir", command=salir)
boton_salir.pack(side=tk.LEFT, padx=5, pady=5)

boton_ver_todo = tk.Button(marco_contenido, text="ver toda la Base de datos", command=mostrar_db_entera)
boton_ver_todo.pack(side=tk.LEFT, padx=5, pady=5)
# Preguntar si mostrar la base de datos al iniciar
def iniciar():
    visualizar_init = ask_custom_string("Ver BBDD completa", "Elige: y / n").lower()
    if visualizar_init == 'y':
        mostrar_db_entera()
    elif visualizar_init == 'n':
        pass
    else:
        while visualizar_init not in ('y', 'n'):
            visualizar_init = ask_custom_string("Ver BBDD completa", "Elige: y / n").lower()
iniciar()
#mostrar_db_entera()

# Guardar el db antes de salir
def on_closing():
    with open(ruta_completa, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False)
    ventana.destroy()

ventana.protocol("WM_DELETE_WINDOW", on_closing)
ventana.mainloop()
