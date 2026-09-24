"""Capa de lógica de negocio: registro (RF-09), descuento de stock (RF-10)
y alerta de stock mínimo (RF-11) mediante el patrón Observer."""
from typing import Callable

from .modelo import Repuesto
from .repositorio import RepuestoRepositorio


class StockInsuficienteError(Exception):
    """Se lanza cuando se intenta descontar más unidades de las disponibles."""


class InventarioServicio:
    def __init__(self, repositorio: RepuestoRepositorio):
        self._repositorio = repositorio
        self._observadores: list[Callable[[Repuesto], None]] = []

    # --- Patrón Observer ---
    def suscribir(self, observador: Callable[[Repuesto], None]) -> None:
        self._observadores.append(observador)

    def _notificar(self, repuesto: Repuesto) -> None:
        for observador in self._observadores:
            observador(repuesto)

    # --- RF-09 ---
    def registrar(self, repuesto: Repuesto) -> None:
        if self._repositorio.existe(repuesto.codigo):
            raise ValueError(f"Ya existe un repuesto con el código {repuesto.codigo}.")
        self._repositorio.guardar(repuesto)

    # --- RF-10 y RF-11 ---
    def descontar(self, codigo: str, cantidad: int) -> Repuesto:
        if cantidad <= 0:
            raise ValueError("La cantidad a descontar debe ser mayor que cero.")
        repuesto = self._repositorio.buscar(codigo)
        if repuesto is None:
            raise KeyError(f"No existe el repuesto con código {codigo}.")
        if cantidad > repuesto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente de {repuesto.nombre}: hay {repuesto.stock}, se piden {cantidad}."
            )
        repuesto.stock -= cantidad
        self._repositorio.guardar(repuesto)
        if repuesto.en_stock_minimo:
            self._notificar(repuesto)
        return repuesto

    def repuestos_en_minimo(self) -> list[Repuesto]:
        return [r for r in self._repositorio.listar() if r.en_stock_minimo]
