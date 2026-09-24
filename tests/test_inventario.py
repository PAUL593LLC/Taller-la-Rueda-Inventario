import pytest

from inventario import InventarioServicio, Repuesto, RepuestoRepositorio, StockInsuficienteError


@pytest.fixture
def servicio():
    repositorio = RepuestoRepositorio(":memory:")
    yield InventarioServicio(repositorio)
    repositorio.cerrar()


def filtro_aceite(stock=10, minimo=3):
    return Repuesto("FA-001", "Filtro de aceite", 4.50, 7.00, stock, minimo)


# RF-09
def test_registra_repuesto_con_todos_sus_datos(servicio):
    servicio.registrar(filtro_aceite())
    guardado = servicio._repositorio.buscar("FA-001")
    assert guardado.nombre == "Filtro de aceite"
    assert guardado.precio_venta == 7.00
    assert guardado.stock == 10


def test_no_registra_repuesto_sin_codigo():
    with pytest.raises(ValueError):
        Repuesto("", "Bujía", 2.0, 3.5, 5)


def test_no_permite_codigo_repetido(servicio):
    servicio.registrar(filtro_aceite())
    with pytest.raises(ValueError):
        servicio.registrar(filtro_aceite())


# RF-10
def test_descuenta_stock_al_usar_repuesto(servicio):
    servicio.registrar(filtro_aceite(stock=10))
    servicio.descontar("FA-001", 4)
    assert servicio._repositorio.buscar("FA-001").stock == 6


def test_no_permite_stock_negativo(servicio):
    servicio.registrar(filtro_aceite(stock=2))
    with pytest.raises(StockInsuficienteError):
        servicio.descontar("FA-001", 5)
    assert servicio._repositorio.buscar("FA-001").stock == 2


# RF-11
def test_alerta_cuando_llega_al_minimo(servicio):
    alertas = []
    servicio.suscribir(alertas.append)
    servicio.registrar(filtro_aceite(stock=5, minimo=3))
    servicio.descontar("FA-001", 2)
    assert len(alertas) == 1 and alertas[0].stock == 3


def test_no_alerta_si_el_stock_es_suficiente(servicio):
    alertas = []
    servicio.suscribir(alertas.append)
    servicio.registrar(filtro_aceite(stock=10, minimo=3))
    servicio.descontar("FA-001", 1)
    assert alertas == []
    assert servicio.repuestos_en_minimo() == []
