"""Patrón DAO: único punto de acceso a la base de datos SQLite."""
import sqlite3
from typing import Optional

from .modelo import Repuesto


class RepuestoRepositorio:
    def __init__(self, ruta_bd: str = "taller_la_rueda.db"):
        self._conexion = sqlite3.connect(ruta_bd)
        self._conexion.execute(
            """CREATE TABLE IF NOT EXISTS repuestos (
                   codigo TEXT PRIMARY KEY,
                   nombre TEXT NOT NULL,
                   precio_compra REAL NOT NULL,
                   precio_venta REAL NOT NULL,
                   stock INTEGER NOT NULL,
                   stock_minimo INTEGER NOT NULL)"""
        )
        self._conexion.commit()

    def guardar(self, repuesto: Repuesto) -> None:
        self._conexion.execute(
            "INSERT OR REPLACE INTO repuestos VALUES (?, ?, ?, ?, ?, ?)",
            (repuesto.codigo, repuesto.nombre, repuesto.precio_compra,
             repuesto.precio_venta, repuesto.stock, repuesto.stock_minimo),
        )
        self._conexion.commit()

    def existe(self, codigo: str) -> bool:
        return self.buscar(codigo) is not None

    def buscar(self, codigo: str) -> Optional[Repuesto]:
        fila = self._conexion.execute(
            "SELECT codigo, nombre, precio_compra, precio_venta, stock, stock_minimo "
            "FROM repuestos WHERE codigo = ?", (codigo,)
        ).fetchone()
        return Repuesto(*fila) if fila else None

    def listar(self) -> list[Repuesto]:
        filas = self._conexion.execute(
            "SELECT codigo, nombre, precio_compra, precio_venta, stock, stock_minimo "
            "FROM repuestos ORDER BY nombre"
        ).fetchall()
        return [Repuesto(*f) for f in filas]

    def cerrar(self) -> None:
        self._conexion.close()
