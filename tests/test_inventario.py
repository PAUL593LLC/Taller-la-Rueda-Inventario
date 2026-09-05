"""Pruebas automatizadas del módulo de gestión de inventario de repuestos.

Cada prueba corresponde a un caso documentado en el plan de pruebas del
Avance 3. El caso crítico es CP-05, porque verifica que el descuento de
existencias queda guardado en el repositorio y no solo aplicado en memoria.

Ejecución local:  python -m pytest -v
"""

import pytest

from inventario.modelo import Repuesto, StockInsuficienteError
from inventario.repositorio import RepuestoDAO
from inventario.servicio import ServicioInventario


@pytest.fixture
def servicio():
    """Servicio de inventario vacío, con su repositorio y su panel de alertas."""
    return ServicioInventario(RepuestoDAO())


@pytest.fixture
def filtro_registrado(servicio):
    """Repuesto FIL-001 con 10 unidades en stock y nivel mínimo 3."""
    servicio.registrar_repuesto(
        codigo="FIL-001",
        nombre="Filtro de aceite",
        precio_compra=4.50,
        precio_venta=8.00,
        stock=10,
        stock_minimo=3,
    )
    return servicio


# --------------------------- Pruebas unitarias ---------------------------

def test_cp01_no_permite_codigo_de_repuesto_duplicado(filtro_registrado):
    """CP-01 (RF-09): el código del repuesto no puede repetirse."""
    with pytest.raises(ValueError) as error:
        filtro_registrado.registrar_repuesto(
            codigo="FIL-001",
            nombre="Filtro de aceite alterno",
            precio_compra=5.00,
            precio_venta=9.00,
            stock=4,
        )

    assert "FIL-001" in str(error.value)
    assert len(filtro_registrado.dao.listar()) == 1


def test_cp02_descuenta_las_unidades_consumidas():
    """CP-02 (RF-10): descontar 3 unidades de un stock de 10 deja 7."""
    repuesto = Repuesto("PAS-002", "Pastillas de freno", 12.00, 20.00, 10, 2)

    restante = repuesto.descontar_stock(3)

    assert restante == 7
    assert repuesto.stock == 7


def test_cp03_rechaza_consumir_mas_unidades_de_las_disponibles():
    """CP-03 (RF-10): el stock nunca puede quedar negativo."""
    repuesto = Repuesto("PAS-002", "Pastillas de freno", 12.00, 20.00, 10, 2)

    with pytest.raises(StockInsuficienteError):
        repuesto.descontar_stock(12)

    assert repuesto.stock == 10


def test_cp04_avisa_cuando_el_stock_llega_al_nivel_minimo(servicio):
    """CP-04 (RF-11): al tocar el nivel mínimo se emite la alerta."""
    servicio.registrar_repuesto("ACE-003", "Aceite 20W-50", 15.00, 25.00, 4, 3)

    repuesto = servicio.consumir_en_orden("ACE-003", 1)

    assert repuesto.stock == 3
    assert repuesto.en_stock_minimo() is True
    assert len(servicio.panel.alertas) == 1
    assert "ACE-003" in servicio.panel.alertas[0]


# ------------------------- Pruebas de integración -------------------------

def test_cp05_el_descuento_queda_guardado_en_el_repositorio(filtro_registrado):
    """CP-05 (RF-07, RF-10) — CASO CRÍTICO.

    Comprueba que la capa de lógica y el repositorio DAO trabajan juntos: si el
    descuento solo ocurriera en memoria, el inventario del taller quedaría
    descuadrado y la alerta de stock mínimo nunca se dispararía.
    """
    filtro_registrado.consumir_en_orden("FIL-001", 7)

    guardado = filtro_registrado.dao.buscar_por_codigo("FIL-001")

    assert guardado is not None
    assert guardado.stock == 3


def test_cp06_solo_alerta_los_repuestos_que_llegaron_al_minimo(servicio):
    """CP-06 (RF-11): la alerta no se dispara sobre repuestos con existencia suficiente."""
    servicio.registrar_repuesto("FIL-001", "Filtro de aceite", 4.50, 8.00, 10, 3)
    servicio.registrar_repuesto("PAS-002", "Pastillas de freno", 12.00, 20.00, 8, 2)
    servicio.registrar_repuesto("BUJ-004", "Bujía", 3.00, 6.00, 20, 5)

    servicio.consumir_en_orden("PAS-002", 6)

    en_alerta = servicio.repuestos_en_alerta()

    assert [r.codigo for r in en_alerta] == ["PAS-002"]
    assert len(servicio.panel.alertas) == 1
