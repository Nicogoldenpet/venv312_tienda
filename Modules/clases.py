#Fecha: 17/06/2024
#Centro de Biotecnología Agropecuario
#Ficha: 2877795
#Aprendiz: Nicolás Agamez Melo
#Versión 3.12.3

#Importando las librerias y el archivo json para leer los productos
import os
from prettytable import PrettyTable
from colorama import Fore,init, just_fix_windows_console
import Modules.functions as functions
import json

#EN ESTE MÓDULO SE ENCONTRARÁN LAS CLASES QUE CONFORMARÁN LA TIENDA SENA

class Producto: #Creando la clase Producto
    def __init__(self, codigo=0, nombre='', inventario=0, precio=0): #Método constructor
        self.__codigo=codigo
        self.__nombre=nombre
        self.__inventario=inventario
        self.__precio=precio
        
    #Métodos getter y setter para los valores
    def get__codigo(self):
        return self.__codigo
    
    
    def set__codigo(self, value):
        self.__codigo = value
        
        
    def get__nombre(self):
        return self.__nombre
    
    
    def set__nombre(self, value):
        self.__nombre = value
        
        
    def get__inventario(self):
        return self.__inventario
    
    
    def set__inventario(self, value):
        self.__inventario = value
        
        
    def get__precio(self):
        return self.__precio
    
    
    def set__precio(self, value):
        self.__precio = value


class ProductosVenta: #Creando la clase ProductosVenta

    def __init__(self, listaproductos: list = []): #Método constructor para crear la lista de productos vacia
        self.__listaproductos=listaproductos
        
    #Método setter para la lista
    def get__listaproductos(self):
        return self.__listaproductos    
    
    
    def cargar_archivos_productos(self): #Mostrando los archivos cargados desde JSON
        tabla = """
+--------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                                            |
|                                                       PRODUCTOS CARGADOS DESDE EL ARCHIVO                                                  | 
|____________________________________________________________________________________________________________________________________________|
|                                                                                                                                            |
|    Código                   Nombre                                                       Inventario                   Precio               |
|____________________________________________________________________________________________________________________________________________|
""" 
    
        with open("./datos.json", "r") as json_file:
            
            data = json.load(json_file) #Abriendo el archivo JSON
            
            for lista in data: #Recorriendo cada diccionario
                producto = Producto()      
                producto.set__codigo(lista["codigo"])
                producto.set__nombre(lista["nombre"])
                producto.set__inventario(lista["inventario"])
                producto.set__precio(lista["precio"])
                self.__listaproductos.append(producto)
                tabla = tabla + "{4:<4} {0:<25}{1:<61}{2:<28} ${3:<19} {4}\n".format( #Ajustando la tabla con .format
                    producto.get__codigo(),
                    producto.get__nombre(), 
                    producto.get__inventario(), 
                    producto.get__precio(), "|")
            tabla = tabla + """
|____________________________________________________________________________________________________________________________________________|
            """
            
            print(Fore.LIGHTYELLOW_EX, tabla)
            
            print(Fore.WHITE)
            mensaje = "Presione ESC para continuar..."
            opciones = b'\x1b'
            functions.digite_caracter(mensaje, opciones) #Leyendo un solo caracter   
            
            
    def carga_manual_productos(self): #Cargando los nuevos productos
        resp = b'S'
        while resp == b'S':
            os.system("cls")
            self.productos_existentes()
            self.__listaproductos.append(self.nuevos_productos())
            print(Fore.LIGHTYELLOW_EX)
            mensaje = "¿Quiere grabar más datos? (S/N)"
            opciones = [b'S', b'N']
            resp = functions.digite_caracter(mensaje, opciones) #Leyendo dos únicas respuestas
            
            
    def borrar_productos(self): #Definiendo una función para borrar productos
        while True:
            os.system("cls")
            self.productos_existentes() #Mostrando los productos existentes
            print(Fore.LIGHTYELLOW_EX)
            code = input("Ingrese el código del producto que desee borrar: ")  # Leyendo el código del producto
            producto_encontrado = False

            for producto in self.get__listaproductos():
                if code == producto.get__codigo(): #Si el código otorgado es igual a alguno de los que hay en la tienda...
                    producto_encontrado = True
                    print(Fore.WHITE)
                    print("DATOS DEL PRODUCTO") #Muestra los datos del producto antes de borrarlo
                    print("NOMBRE: {0}".format(producto.get__nombre()))
                    print("INVENTARIO: {0}".format(producto.get__inventario()))
                    print("PRECIO: ${0}".format(producto.get__precio()))
                    print(Fore.LIGHTYELLOW_EX)

                    mensaje = "¿Desea eliminar el producto? (S/N)"
                    opciones = [b'S', b'N']
                    resp = functions.digite_caracter(mensaje, opciones) #Leyendo dos únicas respuestas

                    if resp == b'S': #Si la respuesta es "S" elimina el producto de la lista
                        self.get__listaproductos().remove(producto)
                        print("Producto eliminado exitosamente.")
                        print("")
                    break

            if not producto_encontrado: #Si no encuentra ningún producto...
                print(Fore.LIGHTYELLOW_EX)
                print("No se encontró un producto con el código proporcionado.") #Ps no jajajaj
                print("")
                    
            mensaje = "¿Desea eliminar otro producto? (S/N): " #Preguntando si desea eliminar más productos
            opciones = [b'S', b'N']
            resp = functions.digite_caracter(mensaje, opciones)
            if resp == b'N':
                break

        os.system("cls")
        self.productos_existentes()  # Mostrando la lista actualizada de productos
        
        
    def nuevos_productos(self): #Creando una función para leer los nuevos productos
        
        productos = Producto() #Instanciando desde la clase Producto()
        
        while True:
            print(Fore.WHITE)
            code = input("Ingrese el código del producto (para mayor comodidad ingrese 3 ceros al inicio): ") #Leyendo el código
            if code.isdigit() and len(code) == 5: #Verificando que se lea como un código
                resp = self.verificar_codigo(code)
                if resp:
                    break
                
        productos.set__codigo(code) #Guardando el código
        
        
        while True:
            name = input("Ingrese el nombre del producto: ") #Leyendo el nombre
            if len(name) < 35: #Verificando que se lea como un nombre
                resp = self.verificar_nombre(name)
                if resp:
                    break
                
        productos.set__nombre(name.upper()) #Guardando el nombre
        
        
        while True:
            inventory = input("Ingrese la cantidad de dicho producto a su disposición: ") #Leyendo el inventario
            if inventory.isdigit(): #Verificando que se lea como inventario
                inventory = int(inventory)
                break
            
        productos.set__inventario(inventory) #Guardando el inventario
        
        
        while True:
            cash = input("Ingrese el precio del producto: ") #Leyendo el precio
            if cash.isdigit(): #Verificando que se lea como precio
                cash = int(cash)
                break
            
        productos.set__precio(cash) #Guardando el precio
        
        
        return productos #Retornando el producto
    
        
    def verificar_codigo(self, dato): #Verificando que no exista un código repetido
        valor_aprobado = True
        for objeto in self.get__listaproductos():
            if objeto.get__codigo() == dato:
                valor_aprobado = False
                break
        return valor_aprobado    
    
    
    def verificar_nombre(self, dato): #Verificando que no exista un nombre repetido 
        valor_aprobado = True
        for objeto in self.get__listaproductos():
            if objeto.get__nombre() == dato:
                valor_aprobado = False
                break
        return valor_aprobado
        
        
    def productos_existentes(self): #Definiendo la función para mostrar los productos disponibles de la tienda SENA
        tabla = """
+--------------------------------------------------------------------------------------------------------------------------------------------+
|                                                                                                                                            |
|                                                    PRODUCTOS DISPONIBLES DE LA TIENDA SENA                                                 | 
|____________________________________________________________________________________________________________________________________________|
|                                                                                                                                            |
|    Código                   Nombre                                                       Inventario                   Precio               |
|____________________________________________________________________________________________________________________________________________|
"""
        for lista in ProductosVenta.get__listaproductos(self):       
            tabla = tabla + "{4:<4} {0:<25}{1:<61}{2:<28} ${3:<19} {4} \n".format(
                    lista.get__codigo(),
                    lista.get__nombre(), 
                    lista.get__inventario(), 
                    lista.get__precio(), "|")
        tabla = tabla + """
|____________________________________________________________________________________________________________________________________________|
        """
        
        print(Fore.LIGHTYELLOW_EX, tabla)


    def guardar_productos(self): #Definiendo la función para guardar los productos
        with open("./datos.json", "w") as json_file:
            
            productos_guardados = []
            for producto in self.get__listaproductos(): #Recorriendo los datos de la lista
                productos_guardados.append({
                    'codigo': producto.get__codigo(),
                    'nombre': producto.get__nombre(),
                    'inventario': producto.get__inventario(),
                    'precio': producto.get__precio()
                })
            json.dump(productos_guardados, json_file, indent=4) #Guardando los productos de la lista en el formato json para cerrar el programa


class ProductoCarrito: #Creando la clase ProductoCarrito
    def __init__(self, codigo=0, nombre='', cantidad=0, precio=0, subtotal=0): #Método constructor
        self.__codigo=codigo
        self.__nombre=nombre
        self.__cantidad=cantidad
        self.__precio=precio
        self.__subtotal=subtotal
        
    #Métodos getter y setter para los valores
    def get__codigo(self):
        return self.__codigo
    
    
    def set__codigo(self, value):
        self.__codigo = value
        
        
    def get__nombre(self):
        return self.__nombre
    
    
    def set__nombre(self, value):
        self.__nombre = value
        
        
    def get__cantidad(self):
        return self.__cantidad
    
    
    def set__cantidad(self, value):
        self.__cantidad = value
        
        
    def get__precio(self):
        return self.__precio
    
    
    def set__precio(self, value):
        self.__precio = value


    def get__subtotal(self):
        return self.__subtotal
    
    
    def set__subtotal(self, value):
        self.__subtotal = value
        
        
    def nuevo_producto(self, productos, carrito_compra): #Definiendo la función para comprar un producto
        while True:
            os.system("cls")
            productos.productos_existentes()
            print(Fore.LIGHTYELLOW_EX)
            code = input("Ingrese el código del producto que desee comprar: ")  # Leyendo el código del producto
            producto_encontrado = False

            for producto in productos.get__listaproductos(): #Si el código del producto se encuentra, muestra su información
                if code == producto.get__codigo():
                    producto_encontrado = True
                    comprar = ProductoCarrito()
                    comprar.set__codigo(code)
                    comprar.set__nombre(producto.get__nombre())
                    comprar.set__precio(producto.get__precio())
                    print(Fore.WHITE)
                    print("INFORMACIÓN DEL PRODUCTO")
                    print("NOMBRE: {0}".format(producto.get__nombre()))
                    print("PRECIO: {0}".format(producto.get__precio()))
                    print("UNIDADES DISPONIBLES: {0}".format(producto.get__inventario()))
                    print(Fore.LIGHTYELLOW_EX)
                    unidades = input("¿Cuántas unidades desea comprar: ")
                    print("")

                    if unidades.isdigit() and int(unidades) <= producto.get__inventario():
                        unidades = int(unidades)
                        subtotal = unidades * producto.get__precio()
                        comprar.set__subtotal(subtotal)
                        comprar.set__cantidad(unidades)
                        # Actualizar el inventario del producto
                        nuevo_inventario = int(producto.get__inventario()) - unidades
                        producto.set__inventario(nuevo_inventario)
                        # Añadir al carrito
                        carrito_compra.append(comprar)
                        print("Se añadió al carrito")
                        # Mostrar el total del carrito
                        total = sum(item.get__subtotal() for item in carrito_compra) #Definiendo el total del carrito
                        print(f"El total de su carrito es: ${total}")

                    else:
                        print("Cantidad no válida")

            if not producto_encontrado:
                print("No se encontró un producto con el código proporcionado.")
                print("")
                    
            mensaje = "¿Desea comprar más productos? (S/N): "
            opciones = [b'S', b'N']
            resp = functions.digite_caracter(mensaje, opciones)
            if resp == b'N':
                break    


class CarritoCompra:
    def __init__(self, documento=0, nombre='', direccion='', productoscarrito: list = []): #Método constructor
        self.__documento=documento
        self.__nombre=nombre
        self.__direccion=direccion
        self.__productoscarrito=productoscarrito

        #Métodos getter y setter para los valores
    def get__documento(self):
        return self.__documento
    
    
    def set__documento(self, value):
        self.__documento = value
        
        
    def get__nombre(self):
        return self.__nombre
    
    
    def set__nombre(self, value):
        self.__nombre = value
        
        
    def get__direccion(self):
        return self.__direccion
    
    
    def set__direccion(self, value):
        self.__direccion = value
        
        
    def get__productoscarrito(self):
        return self.__productoscarrito
    
    
    def set__productoscarrito(self, value):
        self.__productoscarrito = value
        
    def datoscompra(self): #Definiendo una función para leer los datos del cliente
        while True:
                print(Fore.WHITE)
                documento = input("Ingrese su documento: ") #Leyendo el documento
                if documento.isdigit(): #Verificando que se lea como un documento
                    break
                    
        self.set__documento(documento) #Guardando el documento
        
        while True:
            nombre = input("Ingrese su nombre: ") #Leyendo el nombre
            break
        self.set__nombre(nombre) #Guardando el nombre
        
        while True:
            direccion = input("Ingrese su dirección: ") #Leyendo la dirección
            break
        self.set__direccion(direccion) #Guardando la dirección
        
        print(Fore.LIGHTYELLOW_EX)
        print("Compra realizada, para ver su factura digite la opción 7 en el menú.")
        print("¡Vuelva pronto!")
        mensaje = "Presione ESC para continuar..."
        opciones = b'\x1b'
        functions.digite_caracter(mensaje, opciones) #Leyendo un solo caracter   
        return self
        

    def imprimir_factura(self): #Imprimiendo la factura del cliente
        os.system("cls")
        print("////////////////////////////////////////////////////////////////////////////")
        print("                                                                            ")
        print("                               FACTURA DE COMPRA                            ")
        print("                                                                            ")
        print("////////////////////////////////////////////////////////////////////////////")
        print("")
        print(Fore.LIGHTYELLOW_EX)
        print(f" DOCUMENTO: {self.__documento}")
        print(f" NOMBRE: {self.__nombre}")
        print(f" DIRECCIÓN: {self.__direccion}")
        print(Fore.WHITE)
        print("")

        table = PrettyTable() #Creando la tabla con PrettyTable
        table.field_names = ["Código", "Nombre", "Unidades", "Precio Unitario", "Subtotal"]
        for item in self.__productoscarrito:
            table.add_row([item.get__codigo(), item.get__nombre(), item.get__cantidad(), item.get__precio(), item.get__subtotal()])

        print(" PRODUCTOS COMPRADOS:")
        print(Fore.LIGHTCYAN_EX, table)
        print(Fore.LIGHTYELLOW_EX)
        total = sum(item.get__subtotal() for item in self.__productoscarrito)
        print(f" TOTAL A PAGAR: ${total}")
        print(Fore.WHITE, "////////////////////////////////////////////////////////////////////////////")

        print(Fore.LIGHTYELLOW_EX)
        mensaje = "Presione ESC para continuar..."
        opciones = b'\x1b'
        functions.digite_caracter(mensaje, opciones) #Leyendo un solo caracter   