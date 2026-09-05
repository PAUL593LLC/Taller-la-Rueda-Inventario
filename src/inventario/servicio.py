"""Capa de lógica de negocio del módulo de inventario.

Concentra las reglas del taller: registro de repuestos, descuento de stock al
consumirlos en una orden de trabajo y aviso cuando la existencia llega al
nivel mínimo. Se apoya en RepuestoDAO y nunca escribe consultas por su cuenta.
"""

from .modelo import Repuesto
from .repositorio import RepuestoDAO


class PanelAlertaStock:
    """Observador que registra los avisos de stock mínimo (RF-11)."""

    def __init__(self):
        self.alertas: list[str] = []

    def actualizar(self, repuesto: Repuesto) -> None:
        if repuesto.en_stock_minimo():
            self.alertas.append(
                f"El repuesto {repuesto.codigo} ({repuesto.nombre}) llegó al nivel "
                f"mínimo: quedan {repuesto.stock} unidades."
            )


class ServicioInventario:
    """Reglas de negocio del inventario de repuestos."""

    def __init__(self, dao: RepuestoDAO, panel: PanelAlertaStock | None = None):
        self.dao = dao
        self.panel = panel or PanelAlertaStock()

    def registrar_repuesto(
        self,
        codigo: str,
        nombre: str,
        precio_compra: float,
        precio_venta: float,
        stock: int,
        stock_minimo: int = 0,
    ) -> Repuesto:
        """Registra un repuesto nuevo en el inventario (RF-09)."""
        if not codigo.strip():
            raise ValueError("El código del repuesto es obligatorio.")
        if precio_compra < 0 or precio_venta < 0:
            raise ValueError("Los precios no pueden ser negativos.")
        if stock < 0 or stock_minimo < 0:
            raise ValueError("Las cantidades no pueden ser negativas.")

        repuesto = Repuesto(
            codigo=codigo.strip().upper(),
            nombre=nombre.strip(),
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock,
            stock_minimo=stock_minimo,
        )
        repuesto.registrar_observador(self.panel)
        return self.dao.registrar(repuesto)

    def consumir_en_orden(self, codigo: str, cantidad: int) -> Repuesto:
        """Descuenta unidades cuando el repuesto se usa en una orden (RF-07, RF-10)."""
        repuesto = self.dao.buscar_por_codigo(codigo.strip().upper())
        if repuesto is None:
            raise ValueError(f"No existe un repuesto con el código {codigo}.")
        repuesto.descontar_stock(cantidad)
        return self.dao.actualizar(repuesto)

    def repuestos_en_alerta(self) -> list[Repuesto]:
        """Lista los repuestos que están en el nivel mínimo o por debajo (RF-11)."""
        return self.dao.listar_en_stock_minimo()
