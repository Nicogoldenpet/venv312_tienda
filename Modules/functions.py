#Fecha: 17/06/2024
#Centro de Biotecnología Agropecuario
#Ficha: 2877795
#Aprendiz: Nicolás Agamez Melo
#Versión 3.12.3

#EN ESTE MÓDULO SE ENCONTRARÁN LAS FUNCIONES PRINCIPALES QUE CONFORMAN LA TIENDA SENA

#Importando las librerias y archivos
import json
import os
import msvcrt
import datetime
import Modules.clases as clases
from colorama import Fore,init, just_fix_windows_console

intentos_carga = 0
carrito_actual = None

def respuestas(mensaje, opciones): #Definiendo la función de respuestas
    print(mensaje)
    respuesta = 9
    while not respuesta in opciones:
        try:
            respuesta = int(msvcrt.getwch())
        except ValueError:
            respuesta = None
    return respuesta


def digite_caracter(mensaje, opciones): #Definiendo la función para leer un solo caractér
    print(mensaje)
    respuesta = b'\r'
    while not respuesta in opciones:
        respuesta = msvcrt.getch()
    return respuesta


def menu(): #Definiendo la función de menú
    os.system("cls")
    print(Fore.GREEN)
    print("/////////////////////////////////////////////////////////////////")
    print("                                                                 ")
    print("==                 BIENVENIDO A LA TIENDA SENA                 ==")
    print("                                                                 ")
    print("/////////////////////////////////////////////////////////////////")
    print(Fore.WHITE)
    print("*************         1. CARGAR DATOS                 ***********")
    print("*************         2. COPIA DE RESPALDO            ***********")
    print("*************         3. REPARAR DATOS                ***********")
    print("*************         4. GRABAR NUEVOS PRODUCTOS      ***********")
    print("*************         5. BORRAR PRODUCTO              ***********")
    print("*************         6. COMPRAR PRODUCTOS            ***********")
    print("*************         7. IMPRIMIR FACTURA             ***********")
    print("*************         0. SALIR                        ***********")
    print("")


def copia_respaldo(): #Definiendo la función para una copia de respaldo
    os.system("cls")

    print(Fore.LIGHTYELLOW_EX)

    original_json_path = './datos.json' #Ruta de archivo JSON original

    today = datetime.date.today()
    backup_file_name = f"datos_{today.strftime('%d-%m-%Y')}.json" #Obteniendo la fecha actual para la copia del archivo

    backup_json_path = f"./{backup_file_name}" #Definiendo la ruta de respaldo

    with open(original_json_path, 'r') as json_file: #Leyendo el archivo json original
        original_data = json.load(json_file)

    backup_data = original_data.copy() #Creando una copia de los datos originales

    with open(backup_json_path, 'w') as json_file: #Guardando el respaldo del archivo json
        json.dump(backup_data, json_file, indent=4)

    print(f"Se ha creado una copia de respaldo del archivo JSON en: {backup_json_path}")

    print(Fore.GREEN)
    backup_files = [f for f in os.listdir('./') if f.startswith('datos_') and f.endswith('.json')] #Mostrando las copias de seguridad disponibles
    print("Copias de seguridad disponibles:")
    for i, file in enumerate(backup_files, start=1):
        print(f"{i}. {file}")

    print(Fore.LIGHTYELLOW_EX)
    mensaje = "Presione ESC para continuar..."
    opciones = b'\x1b'
    digite_caracter(mensaje, opciones)
    
    
def cargar_datos(): #Definiendo la función de cargar datos
    os.system("cls")

    global intentos_carga #Creando la variable de intentos globales
    
    if intentos_carga > 0:
        print(Fore.LIGHTYELLOW_EX, "Ya se han cargado los datos anteriormente.")
        mensaje = "Presione ESC para continuar..."
        opciones = b'\x1b'
        digite_caracter(mensaje, opciones)
        productos = clases.ProductosVenta()
        return productos  # Retornando la lista de productos sin crear otra
    
    productos = clases.ProductosVenta() #Creando la lista de productos una única vez
    productos.cargar_archivos_productos()
    intentos_carga += 1
    return productos
        
        
def nuevos_productos(productos): #Definiendo la función para nuevos productos
    os.system("cls")
    productos.productos_existentes()
    productos.carga_manual_productos()
    
    
def borrar_productos(productos): #Definiendo la función para borrar productos
    os.system("cls")
    productos.borrar_productos()


def comprar_productos(productos): #Definiendo la función para comprar productos
    global carrito_actual #Instancia para la compra actual del cliente
    os.system("cls")
    carrito_compra = []  # Definir carrito_compra como una lista vacía
    producto = clases.ProductoCarrito() #Instancia para la compra de productos
    producto.nuevo_producto(productos, carrito_compra)

    # Solicitar datos del cliente
    carrito_actual = clases.CarritoCompra() #Instancia para los datos del cliente
    carrito_actual.datoscompra()
    carrito_actual.set__productoscarrito(carrito_compra) #Seteando la lista de productos como el carrito del cliente


def imprimir_factura(): #Definiendo la función para imprimir la factura
    global carrito_actual
    if carrito_actual:
        os.system("cls")
        carrito_actual.imprimir_factura() #Si se encuentra una compra en el carrito se muestra en pantalla
    else:
        os.system("cls")
        print(Fore.LIGHTYELLOW_EX,"No hay compras registradas.")
        mensaje = "Presione ESC para continuar..."
        opciones = b'\x1b'
        digite_caracter(mensaje, opciones) #Leyendo un solo caracter

    
def cerrar_app(productos): #Definiendo la función para cerrar la app
    os.system("cls")
    cantidad_productos = len(productos.get__listaproductos())
    productos.guardar_productos()  # Guardar productos en el archivo JSON
    print(Fore.GREEN)
    print("/////////////////////////////////////////////")
    print("                                             ")
    print(f"==      SE HAN GUARDADO {cantidad_productos} PRODUCTOS        ==") #Mostrando la cantidad de productos guardados al salir
    print("               ¡HASTA PRONTO!                ")
    print("                                             ")
    print("/////////////////////////////////////////////")


def reparar_datos(): #Definiendo la función para reparar datos
    os.system("cls")
    backup_files = [f for f in os.listdir('./') if f.startswith('datos_') and f.endswith('.json')]
    print(Fore.LIGHTYELLOW_EX, "Copias de seguridad disponibles: ")
    print(Fore.WHITE)
    for i, file in enumerate(backup_files, start=1):
        print(f"{i}. {file}")

    while True:
        print("")
        choice = input("Ingrese el número de la copia de seguridad que desea usar: ")
        try:
            index = int(choice)
            if 1 <= index <= len(backup_files):
                chosen_file = backup_files[index - 1]
                original_json_path = f'./{chosen_file}'
                os.rename(original_json_path, './datos.json')
                break
            else:
                print(Fore.RED,"Número invalido. Intentelo de nuevo.")
                print(Fore.WHITE)
        except FileExistsError:
            mensaje = "El archivo datos.json está en existencia, ¿Le gustaría cambiarlo de todas formas? (S/N): " #Preguntando si desea eliminar más productos
            opciones = [b'S', b'N']
            resp = digite_caracter(mensaje, opciones)
            if resp == b'N':
                break
            os.remove('./datos.json')
            os.rename(original_json_path, './datos.json')
            break
        except ValueError:
            print(Fore.RED,"Entrada invalida. Intentelo de nuevo.")
            print(Fore.WHITE)
    

    mensaje = "Presione ESC para continuar..."
    opciones = b'\x1b'
    digite_caracter(mensaje, opciones)