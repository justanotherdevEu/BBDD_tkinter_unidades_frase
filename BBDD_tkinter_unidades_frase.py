import tkinter as tk
import json, os
from tkinter import messagebox

# Ruta al archivo TXT
filename = "unidades_fraseologicas.txt"
# Inicializamos el diccionario vacío
db = {}   # es necesario que db sea una variable global, no sólo de algunos bucles y funciones

ruta = os.getcwd()  # la librería trabaja con comandos del sistema, con la funcion os.getcwd() obetenemos el directorio donde trabajamos ahora

if os.name == "posix":
    #print("No es Linux")
    print("\tEste sistema es Linux, es necesario Windows")
    
elif os.name == "nt":
    print("\t\tTodo bien, este sistema es Windows")
# Encuentra la posición del directorio 'Users' en la ruta
pos = ruta.index('Users')


# Trunca la ruta hasta 'Users/(usuario)/'
user_dir = ruta[:pos] + ruta[pos:ruta.index('\\', pos+6)+1]
#       print("user_dir:\t"+str(user_dir))
# Añade 'Downloads' a la ruta
downloads_dir = os.path.join(user_dir, 'Downloads')

# Cambia al directorio de descargas
os.chdir(downloads_dir)
#print("downloads_dir\t"+downloads_dir)
ruta = os.getcwd()
#print("current ruta:\t"+ruta)
ruta_completa = os.path.join(downloads_dir, filename)
# Leer db del archivo TXT
pos = ruta_completa.index("C:")
#print("ruta completa:\t"+ruta_completa)
ruta_completa = ruta_completa[pos:]
#print("ruta_completa [pos:] :\t"+ruta_completa)
try:
    with open(ruta_completa, 'r', encoding='utf-8') as f:
        db = json.load(f)
except: 
    with open(ruta_completa, 'w+', encoding='utf-8') as f:
        f.write("{}")
        if os.path.exists(ruta_completa):
            #json.dump(db, f, ensure_ascii=False)
            db = json.load(f)  # iniciar el diccionario vacío en caso de que hayamos tenido que crear el archivo porque no existe
        del db      # mejor asegurarse de volver a crear de 0 la variable 'db' con el diccionario 
        


# Crear ventana principal
ventana = tk.Tk()
ventana.title("Base de Datos de Unidades Fraseológicas")

# Crear marco para el contenido
marco_contenido = tk.Frame(ventana)
marco_contenido.pack(padx=150, pady=150)
#       mostrar_db_entera()

def borrar_etiquetas():
    # Borrar contenido de la ventana
        for etiqueta in etiquetas:
            etiqueta.destroy()
        etiquetas.clear()  # Limpiar la lista de etiquetas
        #ventana.destroy()  # Destruir la ventana principal
        #   SÓLO DESTRUIR la ventana al terminar del todo el programa
# Mostrar db en etiquetas
etiquetas = []


def mostrar_db_entera():
    for clave, valor in db.items():
        etiqueta_clave = tk.Label(marco_contenido, text=f"Clave: {clave}")
        etiqueta_clave.pack()
        etiquetas.append(etiqueta_clave)

        etiqueta_valor = tk.Label(marco_contenido, text=f"Valor: {valor}")
        etiqueta_valor.pack()
        etiquetas.append(etiqueta_valor)

        # Agregar separador
        separador = tk.Frame(marco_contenido, height=3,width=100, background="black")
        separador.pack(pady=2)
        etiquetas.append(separador)

# Función para manejar el menú
clave = None
valor = None

def manejar_menu(entrada):
    menu = tk.Label(ventana, text="\n1. Añadir\n2. Buscar en claves\n3. Buscar en valores\n4. Buscar en ambos\n5. Borrar pareja clave-valor\n6. Borrar valor de una clave\n7. Borrar un string de una tupla\n8. Salir del programa\n9. Ver la BBDD completa\n\n\tRecuerda que introducir algo que no sea número te retendrá aquí")
    menu.pack()
    opcion = entrada.get()
    #entrada.delete(0, tk.END)
    #entrada.destroy()  # Eliminar el campo de entrada anterior
    if opcion == '1':
        # Crear campo de entrada para "clave"
        clave_user = tk.Entry(ventana)
        clave_user.pack()
        # Crear botón para enviarlo
        def enviar_clave():
            clave = clave_user.get()
            clave_user.destroy()
            # Crear campo de entrada para "valor"
            valor_user = tk.Entry(ventana)
            valor_user.pack()
            # Crear botón para enviarlo
            def enviar_valor():
                valor = valor_user.get()
                valor_user.destroy()
                # Aquí puedes procesar la clave y el valor
                print(f"Clave: {clave}, Valor: {valor}")
            boton_valor = tk.Button(ventana, text='Enviar', command=enviar_valor)
            boton_valor.pack()
        boton_clave = tk.Button(ventana, text="Enviar", command=enviar_clave)
        boton_clave.pack()
        """while clave == None or valor == None:
            enviar_clave()"""
        
        if clave in db.keys():  # comprueba si esa clave introducida ya existe
            if type(db[clave]) is tuple and valor not in db[clave]:
                db[clave] = list(db[clave])
                db[clave].append(valor)
                db[clave] = tuple(db[clave])
            elif clave in db.keys() and (db[clave] is None or db[clave] == ''):  # comprueba si esa clave introducida ya existe y no tiene valor
                db[clave] = valor  # cambia el valor a lo que contenga la variable 'valor', pero sin estar haciendo el if anterior, que convierte al final en tupla añadiendo el valor del usuario, pero el primer elemento str queda en blanco
            elif type(db[clave]) is str and db[clave] != valor:
                db[clave] = [db[clave], valor]  # cambia el valor a una lista que contiene el valor existente y 'valor'
            if db[clave] == [""] or db[clave] == (""):  # esto por si acaso no hay nada en valor
                    db[clave] = valor
                    db[clave] = tuple(db[clave])
        elif db.get(clave) == valor:
                os.system("cls")
                print("\n\n\t Lo siento, pero ya existe una pareja clave-valor que coinciden exactamente con los que acabas de introducir")
        else:
                # Comprueba si el valor ya existe en el diccionario, tanto en uno de los string de una tupla como si está en algún valor string. Pero se hace después de haber comprobado en otro "if" que la clave no existe ya
            comprobador = False
            for k, v in db.items():
                if isinstance(v, tuple):
                # Si el valor es una tupla, comprueba si el valor está en la tupla
                    if valor in v:
                        print(f'La clave {k} tiene un valor que coincide: {v}')
                        comprobador = True
                else:
                # Si el valor no es una tupla, comprueba si el valor coincide
                    if v == valor:
                        print(f'La clave {k} tiene un valor que coincide: {v}')
                        comprobador = True
            if comprobador == False:
                db[clave] = valor
                print("pareja clave-valor añadida correctamente")
# Crear campo de entrada para el menú, DE NUEVO porque sino no se podrá elegir otra cosa del menu
        entrada = tk.Entry(ventana)
        entrada.pack()
    elif opcion == '8':
        borrar_etiquetas()
    elif opcion in list(range(2,7)) or opcion == '9':
        nada = tk.Label(marco_contenido, text="\n\n\t\tlas opciones 2-7 y 9 no funcionan aun")
        nada.pack()
    elif opcion == '' or opcion == None:
        #borrar_etiquetas()
        advertencia = tk.Label(marco_contenido, text="\n\n\t\tElige un opción entre 1 y 9")
        advertencia.pack()
        print("Entrada es:\t"+str(entrada)+"\t y opcion:\t "+str(opcion)+"\ttype(opcion)==\t"+str(type(opcion)))
        """boton_enviar = tk.Button(ventana, text="Enviar")#, command=manejar_menu(entrada))
        boton_enviar.pack()"""
    
# Crear campo de entrada para el menú
entrada = tk.Entry(ventana)
entrada.pack()
mostrar_db_entera()
# Crear botón para enviar la opción del menú, en la función
boton_enviar = tk.Button(ventana, text="Enviar", command=manejar_menu(entrada))
boton_enviar.pack()

#manejar_menu(entrada)

# Crear botón para borrar lo que muestra en ventana
boton_enviar = tk.Button(ventana, text="Limpiar ventana", command=borrar_etiquetas)
boton_enviar.pack()

# Crear botón para salir
boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
boton_salir.pack(pady=10)

# Iniciar bucle principal
ventana.mainloop()