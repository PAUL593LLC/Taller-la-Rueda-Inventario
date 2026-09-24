"""Capa de datos del dominio: entidad Repuesto (RF-09)."""
from dataclasses import dataclass


@dataclass
class Repuesto:
    codigo: str
    nombre: str
    precio_compra: float
    precio_venta: float
    stock: int
    stock_minimo: int = 5

    def __post_init__(self):
        if not self.codigo or not self.codigo.strip():
            raise ValueError("El código del repuesto es obligatorio.")
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre del repuesto es obligatorio.")
        if self.precio_compra < 0 or self.precio_venta < 0:
            raise ValueError("Los precios no pueden ser negativos.")
        if self.stock < 0 or self.stock_minimo < 0:
            raise ValueError("El stock no puede ser negativo.")

    @property
    def en_stock_minimo(self) -> bool:
        return self.stock <= self.stock_minimo
