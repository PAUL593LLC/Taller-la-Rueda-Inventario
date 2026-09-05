"""Capa de datos del módulo de inventario (patrón DAO).

Es el único punto por donde el módulo lee y escribe repuestos. La capa de
lógica de negocio nunca consulta la base de datos directamente: así, cambiar
el motor de almacenamiento no obliga a modificar las reglas del taller.

Esta primera versión guarda los datos en memoria para que el módulo pueda
probarse desde ya. En el Avance 4 se sustituye por la implementación
definitiva sobre la base de datos, respetando la misma interfaz.
"""

from .modelo import Repuesto


class RepuestoDAO:
    """Acceso a los repuestos del inventario."""

    def __init__(self):
        self._repuestos: dict[str, Repuesto] = {}

    def registrar(self, repuesto: Repuesto) -> Repuesto:
        """Guarda un repuesto nuevo. El código no puede repetirse (RF-09)."""
        if repuesto.codigo in self._repuestos:
            raise ValueError(f"Ya existe un repuesto con el código {repuesto.codigo}.")
        self._repuestos[repuesto.codigo] = repuesto
        return repuesto

    def buscar_por_codigo(self, codigo: str) -> Repuesto | None:
        """Devuelve el repuesto solicitado o None si no está registrado."""
        return self._repuestos.get(codigo)

    def listar(self) -> list[Repuesto]:
        """Devuelve todos los repuestos del inventario."""
        return list(self._repuestos.values())

    def listar_en_stock_minimo(self) -> list[Repuesto]:
        """Devuelve los repuestos que llegaron al nivel mínimo (RF-11)."""
        return [r for r in self._repuestos.values() if r.en_stock_minimo()]

    def actualizar(self, repuesto: Repuesto) -> Repuesto:
        """Guarda los cambios de un repuesto ya registrado."""
        if repuesto.codigo not in self._repuestos:
            raise ValueError(f"No existe un repuesto con el código {repuesto.codigo}.")
        self._repuestos[repuesto.codigo] = repuesto
        return repuesto
