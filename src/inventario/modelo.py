"""Entidades del módulo de inventario de repuestos.

Corresponde a la clase Repuesto del diagrama de clases de la Unidad 2.
Se mantiene independiente del framework para que la lógica pueda probarse
de forma automática sin levantar la aplicación completa.
"""

from dataclasses import dataclass, field


class StockInsuficienteError(Exception):
    """Se intenta consumir más unidades de las que existen en el inventario."""


@dataclass
class Repuesto:
    """Repuesto registrado en el inventario del taller (RF-09)."""

    codigo: str
    nombre: str
    precio_compra: float
    precio_venta: float
    stock: int
    stock_minimo: int = 0
    observadores: list = field(default_factory=list, repr=False)

    def registrar_observador(self, observador) -> None:
        """Suscribe un observador a los cambios de existencia (patrón Observer)."""
        if observador not in self.observadores:
            self.observadores.append(observador)

    def notificar(self) -> None:
        """Avisa a los suscriptores que la cantidad disponible cambió."""
        for observador in self.observadores:
            observador.actualizar(self)

    def descontar_stock(self, cantidad: int) -> int:
        """Resta unidades del inventario cuando el repuesto se usa en una orden (RF-10)."""
        if cantidad <= 0:
            raise ValueError("La cantidad a descontar debe ser mayor que cero.")
        if cantidad > self.stock:
            raise StockInsuficienteError(
                f"El repuesto {self.codigo} tiene {self.stock} unidades "
                f"y se solicitaron {cantidad}."
            )
        self.stock -= cantidad
        self.notificar()
        return self.stock

    def en_stock_minimo(self) -> bool:
        """Indica si la existencia llegó al nivel mínimo definido (RF-11)."""
        return self.stock <= self.stock_minimo
