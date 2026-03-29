# Tests con pytest para probar el correcto funcionamiento de las clases y métodos implementados en codigov1.py.
import pytest
#Importamos las clases y excepciones del documento de codigo para poder hacer las pruebas.
from codigov1 import (Ubicacion, ClaseNaveEstelar,StockError, RepuestoNoEncontrado, IncompatibilidadError,EstacionEspacial, NaveEstelar, CazaEstelar,Repuesto, Almacen,Nave, UnidadCombate,)

# Definimos fixtures para crear objetos reutilizables en los tests. Esto permite tener un estado inicial consistente para cada prueba y evita la repetición de código.
# Cada fixture devuelve una instancia de la clase correspondiente con atributos predefinidos que se pueden usar en múltiples tests.
@pytest.fixture
def nave_estelar():
    """NaveEstelar básica para pruebas."""
    return NaveEstelar(
        nombre="Executor",
        catalogo=["Motor Iónico", "Escudo"],
        tripulacion=500,
        pasaje=100,
        clase=ClaseNaveEstelar.EJECUTOR,
        id_c="EXEC-01",
        clave=1138,
    )

@pytest.fixture
def caza():
    """CazaEstelar básico para pruebas."""
    return CazaEstelar(
        nombre="TIE Fighter",
        catalogo=["Ala de Caza", "Motor Iónico"],
        id_combate="TIE-99",
        clave=9999,
        dotacion=1,
    )

@pytest.fixture
def estacion():
    """EstacionEspacial básica para pruebas."""
    return EstacionEspacial(
        nombre="Estrella de la Muerte",
        catalogo=["Reactor", "Escudo"],
        tripulacion=1000000,
        pasaje=500000,
        ubicacion=Ubicacion.ENDOR,
    )

@pytest.fixture
def almacen():
    """Almacén con un repuesto de Motor Iónico (5 unidades)."""
    a = Almacen("Base Delta", "Corellia")
    pieza = Repuesto("Motor Iónico", "Kuat Systems", 5, 2500.0)
    a.agregar_repuesto(pieza)
    return a


# Creamos clases de test para organizar las pruebas por funcionalidad. Cada clase contiene métodos de prueba que verifican aspectos específicos del código, como la instanciación de objetos, la herencia, el manejo de excepciones, etc. 

#Tests de instanciación para verificar que los objetos se crean correctamente con los atributos esperados. Cada método de prueba dentro de esta clase se enfoca en una clase específica (NaveEstelar, CazaEstelar, EstacionEspacial, Repuesto, Almacen) y verifica que sus atributos se asignan correctamente al momento de la creación.
class TestInstanciacion:

    def test_nave_estelar_se_crea_correctamente(self, nave_estelar):
        assert nave_estelar.nombre == "Executor"
        assert nave_estelar.tripulacion == 500
        assert nave_estelar.clase == ClaseNaveEstelar.EJECUTOR
        assert nave_estelar.id_combate == "EXEC-01"
        assert nave_estelar.clave_cifrada == 1138

    def test_caza_estelar_se_crea_correctamente(self, caza):
        assert caza.nombre == "TIE Fighter"
        assert caza.dotacion == 1
        assert caza.id_combate == "TIE-99"

    def test_estacion_espacial_se_crea_correctamente(self, estacion):
        assert estacion.nombre == "Estrella de la Muerte"
        assert estacion.ubicacion == Ubicacion.ENDOR
        assert estacion.tripulacion == 1000000

    def test_repuesto_se_crea_con_cantidad_privada(self):
        r = Repuesto("Escudo", "BlasTech", 10, 500.0)
        # La cantidad es privada; solo accesible por getter
        assert r.obtener_cantidad() == 10

    def test_almacen_se_crea_vacio(self):
        a = Almacen("Almacén Norte", "Tatooine")
        assert len(a.inventario) == 0


# Tests de herencia para verificar que las clases NaveEstelar, CazaEstelar y EstacionEspacial heredan correctamente de las clases base Nave y UnidadCombate. Además, se prueban los métodos específicos de cada clase para asegurarse de que funcionan como se espera.

class TestHerencia:

    def test_nave_estelar_es_nave_y_unidad_de_combate(self, nave_estelar):
        assert isinstance(nave_estelar, Nave)
        assert isinstance(nave_estelar, UnidadCombate)

    def test_caza_es_nave_y_unidad_de_combate(self, caza):
        assert isinstance(caza, Nave)
        assert isinstance(caza, UnidadCombate)

    def test_estacion_solo_es_nave(self, estacion):
        assert isinstance(estacion, Nave)
        assert not isinstance(estacion, UnidadCombate)

    def test_mostrar_info_nave_estelar(self, nave_estelar):
        info = nave_estelar.mostrar_info()
        assert "Executor" in info
        assert "Ejecutor" in info

    def test_mostrar_info_caza(self, caza):
        info = caza.mostrar_info()
        assert "TIE Fighter" in info
        assert "1" in info  # probamos la dotacion 

    def test_mostrar_info_estacion_muestra_ubicacion(self, estacion):
        info = estacion.mostrar_info()
        assert "Endor" in info

    def test_transmision_cifrada_nave_estelar(self, nave_estelar):
        msg = nave_estelar.realizar_transmision_cifrada()
        assert "EXEC-01" in msg

    def test_transmision_cifrada_caza(self, caza):
        msg = caza.realizar_transmision_cifrada()
        assert "TIE-99" in msg

# Tests de enumeraciones para verificar que las enumeraciones Ubicacion y ClaseNaveEstelar contienen los valores correctos. Además, se prueba que al crear una EstacionEspacial con una ubicación específica, esa ubicación se refleja correctamente en la información mostrada por el método mostrar_info().

class TestEnumeraciones:

    def test_ubicacion_endor(self):
        assert Ubicacion.ENDOR.value == "Endor"

    def test_clase_nave_eclipse(self):
        assert ClaseNaveEstelar.ECLIPSE.value == "Eclipse"

    def test_estacion_con_ubicacion_raimos(self):
        e = EstacionEspacial("Base X", [], 10, 5, Ubicacion.RAIMOS)
        assert e.ubicacion == Ubicacion.RAIMOS
        assert "Raimos" in e.mostrar_info()

    def test_estacion_con_ubicacion_kaliida(self):
        e = EstacionEspacial("Base Y", [], 10, 5, Ubicacion.KALIIDA)
        assert "Kaliida" in e.mostrar_info()

# Tests de manejo de excepciones para verificar que las excepciones personalizadas StockError, RepuestoNoEncontrado e IncompatibilidadError se lanzan correctamente en situaciones específicas. Cada método de prueba dentro de esta clase se enfoca en una situación particular que debería generar una excepción, como intentar retirar más stock del disponible, solicitar un repuesto que no existe en el almacén o intentar usar una pieza incompatible con la nave.

class TestRepuesto:

    def test_actualizar_stock_suma(self):
        r = Repuesto("Tornillo", "Proveedor A", 10, 1.0)
        r.actualizar_stock(5)
        assert r.obtener_cantidad() == 15

    def test_actualizar_stock_resta(self):
        r = Repuesto("Tornillo", "Proveedor A", 10, 1.0)
        r.actualizar_stock(-3)
        assert r.obtener_cantidad() == 7

    def test_stock_llega_a_cero_sin_error(self):
        r = Repuesto("Tornillo", "Proveedor A", 5, 1.0)
        r.actualizar_stock(-5)
        assert r.obtener_cantidad() == 0

    def test_stock_error_si_resultado_negativo(self):
        """StockError se lanza al intentar retirar más de lo disponible."""
        r = Repuesto("Tornillo", "Proveedor A", 3, 1.0)
        with pytest.raises(StockError):
            r.actualizar_stock(-10)

    def test_stock_no_es_accesible_directamente(self):
        """El atributo privado __cantidad no debe ser accesible por nombre directo."""
        r = Repuesto("Tornillo", "Proveedor A", 5, 1.0)
        assert not hasattr(r, "cantidad")
        assert not hasattr(r, "__cantidad")


## Tests de flujo normal para verificar que las operaciones básicas del Almacen funcionan correctamente. Esto incluye agregar repuestos al inventario, gestionar el mantenimiento de una nave estelar retirando piezas compatibles y verificando que el stock se actualiza correctamente. Además, se verifica que los mensajes de resultado sean adecuados y que el inventario refleje los cambios después de las operaciones.

class TestAlmacenFlujoNormal:

    def test_agregar_repuesto_incrementa_inventario(self, almacen):
        assert len(almacen.inventario) == 1

    def test_mantenimiento_exitoso_reduce_stock(self, almacen, nave_estelar):
        almacen.gestionar_mantenimiento(nave_estelar, "Motor Iónico", 2)
        pieza = almacen.inventario[0]
        assert pieza.obtener_cantidad() == 3

    def test_mantenimiento_exitoso_devuelve_mensaje(self, almacen, nave_estelar):
        resultado = almacen.gestionar_mantenimiento(nave_estelar, "Motor Iónico", 1)
        assert "exitoso" in resultado.lower() or "1" in resultado

    def test_mantenimiento_retira_todo_el_stock(self, almacen, nave_estelar):
        almacen.gestionar_mantenimiento(nave_estelar, "Motor Iónico", 5)
        assert almacen.inventario[0].obtener_cantidad() == 0


# Tests de manejo de excepciones para verificar que las excepciones personalizadas StockError, RepuestoNoEncontrado e IncompatibilidadError se lanzan correctamente en situaciones específicas. Cada método de prueba dentro de esta clase se enfoca en una situación particular que debería generar una excepción, como intentar retirar más stock del disponible, solicitar un repuesto que no existe en el almacén o intentar usar una pieza incompatible con la nave.

class TestAlmacenExcepciones:

    def test_incompatibilidad_pieza_no_en_catalogo(self, almacen, nave_estelar):
        """IncompatibilidadError cuando la pieza no está en el catálogo de la nave."""
        with pytest.raises(IncompatibilidadError):
            almacen.gestionar_mantenimiento(nave_estelar, "Ala de Caza", 1)

    def test_repuesto_no_encontrado_si_no_esta_en_almacen(self, nave_estelar):
        """RepuestoNoEncontrado cuando la pieza es compatible pero no existe en el almacén."""
        almacen_vacio = Almacen("Sin Piezas", "Kashyyyk")
        with pytest.raises(RepuestoNoEncontrado):
            almacen_vacio.gestionar_mantenimiento(nave_estelar, "Motor Iónico", 1)

    def test_stock_error_si_se_pide_mas_del_disponible(self, almacen, nave_estelar):
        """StockError cuando se solicita más cantidad de la que hay en stock."""
        with pytest.raises(StockError):
            almacen.gestionar_mantenimiento(nave_estelar, "Motor Iónico", 100)

    def test_incompatibilidad_tiene_mensaje_descriptivo(self, almacen, nave_estelar):
        with pytest.raises(IncompatibilidadError, match="Ala de Caza"):
            almacen.gestionar_mantenimiento(nave_estelar, "Ala de Caza", 1)

    def test_repuesto_no_encontrado_tiene_mensaje_descriptivo(self, nave_estelar):
        almacen_vacio = Almacen("Sin Piezas", "Kashyyyk")
        with pytest.raises(RepuestoNoEncontrado, match="Motor Iónico"):
            almacen_vacio.gestionar_mantenimiento(nave_estelar, "Motor Iónico", 1)

# Tests de validaciones en el constructor para verificar que al intentar crear una EstacionEspacial con tripulación o pasaje negativo, o un CazaEstelar con dotación negativa, se lance un ValueError. Además, se verifica que una dotación de 0 para un CazaEstelar es válida y se asigna correctamente.

class TestValidacionesConstructor:

    def test_estacion_tripulacion_negativa_lanza_error(self):
        with pytest.raises(ValueError):
            EstacionEspacial("X", [], -1, 100, Ubicacion.ENDOR)

    def test_estacion_pasaje_negativo_lanza_error(self):
        with pytest.raises(ValueError):
            EstacionEspacial("X", [], 100, -1, Ubicacion.ENDOR)

    def test_caza_dotacion_negativa_lanza_error(self):
        with pytest.raises(ValueError):
            CazaEstelar("TIE", [], "ID-01", 111, -5)

    def test_caza_dotacion_cero_es_valida(self):
        """Una dotación de 0 es válida (nave sin tripular)."""
        c = CazaEstelar("TIE-Dron", [], "TIE-00", 0, 0)
        assert c.dotacion == 0


# Tests de escenario complejo para verificar situaciones más realistas donde dos naves comparten el mismo almacén y gestionan el mantenimiento de una pieza compatible. Se verifica que el stock se actualiza correctamente después de cada operación y que el inventario refleja los cambios. Además, se prueba agregar múltiples repuestos al almacén y verificar que el inventario se actualiza con cada adición.

class TestEscenarioComplejo:

    def test_dos_naves_comparten_almacen(self):
        nave1 = NaveEstelar("Devastator", ["Motor Iónico"], 300, 50, ClaseNaveEstelar.ECLIPSE, "EC-01", 111)
        nave2 = CazaEstelar("TIE-Avanzado", ["Motor Iónico"], "TIE-X1", 777, 1)
        almacen = Almacen("Coruscant", "Coruscant")
        almacen.agregar_repuesto(Repuesto("Motor Iónico", "Kuat", 10, 3000.0))

        almacen.gestionar_mantenimiento(nave1, "Motor Iónico", 3)
        almacen.gestionar_mantenimiento(nave2, "Motor Iónico", 2)

        assert almacen.inventario[0].obtener_cantidad() == 5

    def test_agregar_multiple_repuestos(self):
        a = Almacen("Gran Almacén", "Bespin")
        a.agregar_repuesto(Repuesto("Escudo", "BlasTech", 5, 100.0))
        a.agregar_repuesto(Repuesto("Reactor", "Sienar", 3, 900.0))
        assert len(a.inventario) == 2
