from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import List

# Usamos Enum para definir ubicaciones y clases de naves, lo que mejora la legibilidad y evita errores de string.
class Ubicacion(Enum):
    ENDOR = "Endor"
    RAIMOS = "Cúmulo Raimos"
    KALIIDA = "Nebulosa Kaliida"

class ClaseNaveEstelar(Enum):
    EJECUTOR = "Ejecutor"
    ECLIPSE = "Eclipse"
    SOBERANO = "Soberano"

# Definimos excepciones posibles para manejar los errores de manera clara tratando de mantener un orden para los posibles errores de negocio relacionados con el stock y la compatibilidad de piezas.
class StockError(Exception):
    """Se lanza cuando se intenta retirar más stock del disponible."""
    pass

class RepuestoNoEncontrado(Exception):
    """Se lanza cuando el repuesto solicitado no existe en el almacén."""
    pass

class IncompatibilidadError(Exception):
    """Se lanza cuando una nave intenta adquirir un repuesto que no está en su catálogo."""
    pass

# Usamos ABCMeta para definir interfaces abstractas que obligan a implementar ciertos métodos en las clases hijas, asegurando así la consistencia en la implementación de funcionalidades clave como la transmisión cifrada y la presentación de información técnica.
class UnidadCombate(metaclass=ABCMeta):
    """
    Interfaz para unidades de combate.
    Obliga a implementar un método de transmisión cifrada y a tener un identificador de combate y una clave cifrada.
    """
    def __init__(self, id_combate: str, clave_cifrada: int):
        self.id_combate = id_combate
        self.clave_cifrada = clave_cifrada
# El método abstracto 'realizar_transmision_cifrada' asegura que todas las unidades de combate implementen su propia lógica de comunicación segura aunque el detalle de esa lógica quede a criterio de cada clase específica (NaveEstelar, CazaEstelar, etc.). 
    @abstractmethod
    def realizar_transmision_cifrada(self):
        """Método abstracto para obligar a definir un protocolo de comunicación."""
        pass

class Nave(metaclass=ABCMeta):
    """
    Clase base para la flota espacial. 
    Contiene el nombre y el catálogo de piezas compatibles (lista de strings).
    """
    def __init__(self, nombre: str, catalogo_repuestos: List[str]):
        self.nombre = nombre
        self.catalogo_repuestos = catalogo_repuestos
# De nuevo, el método abstracto 'mostrar_info' obliga a que cada tipo de nave implemente su propia forma de presentar su información técnica, lo que es crucial para la gestión y mantenimiento de la flota.
    @abstractmethod
    def mostrar_info(self):
        """Método abstracto para imprimir los detalles técnicos de la nave."""
        pass

# Ahora definimos las clases específicas de naves, cada una con sus atributos y métodos particulares, pero todas heredando de Nave y/o UnidadCombate según corresponda. 
class EstacionEspacial(Nave):
    """
    Estacion espacial fija que sirve como base de operaciones. 
    Tiene atributos específicos como tripulación, pasaje y ubicación.
    """
    def __init__(self, nombre, catalogo, tripulacion, pasaje, ubicacion: Ubicacion):
        super().__init__(nombre, catalogo) # Vemos que se llama al constructor de la clase base Nave para inicializar los atributos comunes(herencia simple).
        if tripulacion < 0 or pasaje < 0:
            raise ValueError("Los valores de personal no pueden ser negativos.")
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.ubicacion = ubicacion

    def mostrar_info(self):
        """Muestra la ubicación actual de la estación usando el valor del Enum."""
        return f"Estación {self.nombre} ubicada en {self.ubicacion.value}"

class NaveEstelar(Nave, UnidadCombate):
    """
    Nave de nivel superior ya que combina características de Nave y UnidadCombate.(herencia múltiple)
    Requiere atributos específicos como tripulación, pasaje y clase de nave.
    """
    def __init__(self, nombre, catalogo, tripulacion, pasaje, clase: ClaseNaveEstelar, id_c, clave):
        Nave.__init__(self, nombre, catalogo)
        UnidadCombate.__init__(self, id_c, clave) # Aquí se llama explícitamente a ambos constructores de las clases base para asegurar que se inicialicen correctamente los atributos de Nave y UnidadCombate.(herencia múltiple)
        self.tripulacion = tripulacion
        self.pasaje = pasaje
        self.clase = clase

    def mostrar_info(self):
        """Devuelve la clase de la nave (Ejecutor, Eclipse, etc.)."""
        return f"Nave Estelar {self.nombre} (Clase: {self.clase.value})"

    def realizar_transmision_cifrada(self):
        """Implementación del método de UnidadCombate."""
        return f"Canal seguro activado para {self.id_combate}."

class CazaEstelar(Nave, UnidadCombate):
    """
    Nave ligera de combate. Requiere el atributo específico 'dotacion'.
    Volvemos a aplicar herencia múltiple para combinar las características de Nave y UnidadCombate, lo que permite que el CazaEstelar tenga tanto un catálogo de piezas compatibles como la capacidad de realizar transmisiones cifradas, además de su dotación específica.
    """
    def __init__(self, nombre, catalogo, id_combate, clave, dotacion):
        Nave.__init__(self, nombre, catalogo)
        UnidadCombate.__init__(self, id_combate, clave)
        if dotacion < 0:
            raise ValueError("La dotación no puede ser negativa.")
        self.dotacion = dotacion

    def mostrar_info(self):
        """Muestra la dotación de pilotos/tripulación técnica."""
        return f"Caza {self.nombre} - Dotación: {self.dotacion}"

    def realizar_transmision_cifrada(self):
        """Implementación del método de UnidadCombate."""
        return f"Caza {self.id_combate} operando en modo sigilo."

# Ahora definimos la clase Repuesto y Almacen, que son fundamentales para la gestión de inventarios y el mantenimiento de las naves. La clase Repuesto tiene un atributo privado para la cantidad, lo que obliga a usar métodos específicos para acceder y modificar el stock, asegurando así un control más riguroso sobre las operaciones de inventario. La clase Almacen gestiona una colección de repuestos y tiene la lógica de negocio para validar la compatibilidad de piezas con las naves y actualizar el stock en consecuencia, lanzando excepciones específicas cuando se presentan errores como falta de stock o incompatibilidad de piezas.
class Repuesto:
    """Objeto que representa una pieza física en el inventario."""
    def __init__(self, nombre, proveedor, cantidad, precio):
        self.nombre = nombre
        self.proveedor = proveedor
        self.__cantidad = cantidad # Atributo privado segun recomendaciones de encapsulamiento del enunciado para proteger la integridad del stock.
        self.precio = precio

    def obtener_cantidad(self):
        """Método getter para acceder al atributo privado __cantidad."""
        return self.__cantidad

    def actualizar_stock(self, cantidad_cambio):
        """
        Modifica el stock sumando o restando. 
        Lanza StockError si el resultado es menor a cero.
        """
        if self.__cantidad + cantidad_cambio < 0:
            raise StockError("No hay suficientes existencias para completar la operación.")
        self.__cantidad += cantidad_cambio

class Almacen:
    """Gestiona la colección de repuestos y su asignación a naves."""
    def __init__(self, nombre, localizacion):
        self.nombre = nombre
        self.localizacion = localizacion
        self.inventario: List[Repuesto] = []

    def agregar_repuesto(self, nuevo_repuesto: Repuesto):
        """Añade un objeto Repuesto a la lista del almacén."""
        self.inventario.append(nuevo_repuesto)

    def gestionar_mantenimiento(self, nave: Nave, nombre_pieza: str, cantidad: int):
        """
        Lógica de negocio principal:
        1. Valida si la pieza es compatible con el catálogo de la nave.
        2. Busca la pieza en el inventario.
        3. Actualiza el stock si todo es correcto.
        """
        # Validación de catálogo (Requisito de integridad)
        if nombre_pieza not in nave.catalogo_repuestos:
            raise IncompatibilidadError(f"La pieza '{nombre_pieza}' no es compatible con {nave.nombre}.")
        
        for item in self.inventario:
            if item.nombre == nombre_pieza:
                item.actualizar_stock(-cantidad)
                return f"Mantenimiento exitoso: {cantidad} unidades de {nombre_pieza} entregadas."
        
        raise RepuestoNoEncontrado(f"La pieza '{nombre_pieza}' no está disponible en este almacén.")

# Prueba de un escenario posible en el main, donde se configuran el almacén, la flota y se procesan órdenes de mantenimiento, demostrando así la funcionalidad completa del sistema de gestión de flota imperial.
if __name__ == "__main__":
    print("=== SISTEMA DE GESTIÓN DE FLOTA IMPERIAL: ESTADO OPERATIVO ===\n")

   # Almacen y stock inicial de repuestos
    almacen_sectorial = Almacen("Complejo Logístico de Kuat", "Sistemas Interiores")
    
    repuestos_iniciales = [
        Repuesto("Reactor de Fusión", "Kuat Drive Yards", 5, 15000),
        Repuesto("Panel Sienar T-7", "Sienar Fleet Systems", 20, 800),
        Repuesto("Módulo de Escudo", "Phylon Freight", 10, 3500)
    ]
    
    for r in repuestos_iniciales:
        almacen_sectorial.agregar_repuesto(r)

    # Despliegue de la Flota (Muestra de Herencia y Polimorfismo)
    # Creamos un ejemplo de cada tipo de nave definida en el enunciado
    flota_imperial = [
        CazaEstelar("Interceptor Alfa", ["Panel Sienar T-7"], "TIE-IN-01", 1122, 1),
        NaveEstelar("Quimera", ["Reactor de Fusión", "Módulo de Escudo"], 35000, 6000, 
                    ClaseNaveEstelar.SOBERANO, "ISD-CHIMERA", 9988),
        EstacionEspacial("Plataforma de Defensa", ["Módulo de Escudo"], 500, 100, Ubicacion.KALIIDA)
    ]

    print("--- REPORTE DE ESTADO DE UNIDADES ---")
    for nave in flota_imperial:
        # Uso del método polimórfico mostrar_info
        print(f"[*] {nave.mostrar_info()}")
        
        # Demostración de capacidades de Unidad de Combate con un chequeo de tipo para evitar errores en tiempo de ejecución al intentar acceder a atributos o métodos que no existen en todas las clases (como la transmisión cifrada que solo tiene sentido para las unidades de combate).
        if isinstance(nave, UnidadCombate):
            print(f"    > Identificador: {nave.id_combate} | {nave.realizar_transmision_cifrada()}")
    
    # Mantenimiento exitoso: Procesamos órdenes de mantenimiento para el caza y el destructor, demostrando la gestión de inventario y la validación de compatibilidad de piezas, así como la actualización del stock en el almacén.
    print("\n--- ÓRDENES DE MANTENIMIENTO PROCESADAS ---")
    caza = flota_imperial[0]
    destructor = flota_imperial[1]

    confirmacion_1 = almacen_sectorial.gestionar_mantenimiento(caza, "Panel Sienar T-7", 4)
    confirmacion_2 = almacen_sectorial.gestionar_mantenimiento(destructor, "Reactor de Fusión", 1)

    print(f"[LOGÍSTICA] {caza.nombre}: {confirmacion_1}")
    print(f"[LOGÍSTICA] {destructor.nombre}: {confirmacion_2}")

    print(f"\n[INVENTARIO ACTUALIZADO] {almacen_sectorial.nombre}:")
    for r in almacen_sectorial.inventario:
        print(f" - {r.nombre}: {r.obtener_cantidad()} unidades disponibles.")

    print("\n--- FIN DEL REPORTE: TODAS LAS UNIDADES OPERATIVAS ---")