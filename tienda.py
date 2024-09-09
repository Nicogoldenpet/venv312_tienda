#Fecha: 17/06/2024
#Centro de Biotecnología Agropecuario
#Ficha: 2877795
#Aprendiz: Nicolás Agamez Melo
#Versión 3.12.3

#EN ESTE CÓDIGO SE ENCONTRARA LA FUNCIÓN PRINCIPAL PARA EJECUTAR LA TIENDA SENA

#Importando los módulos y os
import Modules.functions as functions
import Modules.clases as clases
import os
from colorama import Fore,init, just_fix_windows_console


def main(): #Definiendo la función main
    respuesta = 9 #Definiendo una respuesta que no se usa
    opciones = range(8)
    global productos
    while respuesta!=0: #Mientras que la respuesta sea diferente de 0 podrá ejecutarse cualquiera de las opciones
        os.system("cls")
        functions.menu() #Mostrando el menú
        mensaje = "Por favor seleccione una opción: "
        respuesta = functions.respuestas(mensaje, opciones) #Leyendo la respuesta del usuario
        match respuesta: #Ejecutando la respuesta del usuario
            case 1:
                productos = functions.cargar_datos()
            case 2:
                functions.copia_respaldo()
            case 3:
                functions.reparar_datos()
            case 4:
                functions.nuevos_productos(productos)
            case 5:
                functions.borrar_productos(productos)
            case 6:
                functions.comprar_productos(productos)
            case 7:
                functions.imprimir_factura()
    functions.cerrar_app(productos)


if __name__ == "__main__":
    main() #Ejecutando la función main