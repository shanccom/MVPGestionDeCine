"""Modulo de venta de entradas para el MVP de gestion de cine.

Este archivo es autocontenido para poder trabajar el dominio de ventas sin
crear dependencias hacia otros modulos del sistema.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import sqlite3
from typing import Optional


class VentaError(ValueError):
    """Error de negocio para el modulo de ventas."""


@dataclass(frozen=True)
class Venta:
    id: int
    funcion_id: int
    cantidad_entradas: int
    total: float
    fecha_venta: datetime
    estado: str


class ModuloVentaEntradas:
    """Gestiona la venta y cancelacion de entradas en una base SQLite local."""

    def __init__(self, database_path: str = ":memory:") -> None:
        self._conexion = sqlite3.connect(database_path)
        self._conexion.row_factory = sqlite3.Row
        self._crear_tabla_ventas()

    def cerrar(self) -> None:
        self._conexion.close()

    def _crear_tabla_ventas(self) -> None:
        self._conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS venta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                funcion_id INTEGER NOT NULL,
                cantidad_entradas INTEGER NOT NULL,
                total REAL NOT NULL,
                fecha_venta TEXT NOT NULL,
                estado TEXT NOT NULL DEFAULT 'ACTIVA'
            )
            """
        )
        self._conexion.commit()

    def vender_entradas(
        self,
        funcion_id: int,
        capacidad_sala: int,
        cantidad_entradas: int,
        precio_unitario: float,
    ) -> Venta:
        self._validar_cantidad_entradas(cantidad_entradas)
        self._validar_capacidad_sala(capacidad_sala)
        self._validar_precio_unitario(precio_unitario)

        entradas_vendidas = self._obtener_entradas_vendidas(funcion_id)
        entradas_disponibles = capacidad_sala - entradas_vendidas

        if cantidad_entradas > entradas_disponibles:
            raise VentaError(
                "No se puede registrar la venta: se excede la capacidad disponible."
            )

        total = round(cantidad_entradas * precio_unitario, 2)
        fecha_venta = datetime.now()

        cursor = self._conexion.execute(
            """
            INSERT INTO venta (funcion_id, cantidad_entradas, total, fecha_venta, estado)
            VALUES (?, ?, ?, ?, 'ACTIVA')
            """,
            (
                funcion_id,
                cantidad_entradas,
                total,
                fecha_venta.isoformat(timespec="seconds"),
            ),
        )
        self._conexion.commit()

        return Venta(
            id=cursor.lastrowid,
            funcion_id=funcion_id,
            cantidad_entradas=cantidad_entradas,
            total=total,
            fecha_venta=fecha_venta,
            estado="ACTIVA",
        )

    def cancelar_venta(self, venta_id: int) -> Venta:
        fila = self._conexion.execute(
            """
            SELECT id, funcion_id, cantidad_entradas, total, fecha_venta, estado
            FROM venta
            WHERE id = ?
            """,
            (venta_id,),
        ).fetchone()

        if fila is None:
            raise VentaError("La venta indicada no existe.")

        if fila["estado"] == "CANCELADA":
            raise VentaError("La venta ya fue cancelada.")

        self._conexion.execute(
            "UPDATE venta SET estado = 'CANCELADA' WHERE id = ?",
            (venta_id,),
        )
        self._conexion.commit()

        return Venta(
            id=fila["id"],
            funcion_id=fila["funcion_id"],
            cantidad_entradas=fila["cantidad_entradas"],
            total=fila["total"],
            fecha_venta=datetime.fromisoformat(fila["fecha_venta"]),
            estado="CANCELADA",
        )

    def listar_ventas(self, funcion_id: Optional[int] = None) -> list[Venta]:
        if funcion_id is None:
            filas = self._conexion.execute(
                """
                SELECT id, funcion_id, cantidad_entradas, total, fecha_venta, estado
                FROM venta
                ORDER BY id ASC
                """
            ).fetchall()
        else:
            filas = self._conexion.execute(
                """
                SELECT id, funcion_id, cantidad_entradas, total, fecha_venta, estado
                FROM venta
                WHERE funcion_id = ?
                ORDER BY id ASC
                """,
                (funcion_id,),
            ).fetchall()

        return [
            Venta(
                id=fila["id"],
                funcion_id=fila["funcion_id"],
                cantidad_entradas=fila["cantidad_entradas"],
                total=fila["total"],
                fecha_venta=datetime.fromisoformat(fila["fecha_venta"]),
                estado=fila["estado"],
            )
            for fila in filas
        ]

    def entradas_disponibles(self, funcion_id: int, capacidad_sala: int) -> int:
        self._validar_capacidad_sala(capacidad_sala)
        return capacidad_sala - self._obtener_entradas_vendidas(funcion_id)

    def _obtener_entradas_vendidas(self, funcion_id: int) -> int:
        fila = self._conexion.execute(
            """
            SELECT COALESCE(SUM(cantidad_entradas), 0) AS total_vendido
            FROM venta
            WHERE funcion_id = ? AND estado = 'ACTIVA'
            """,
            (funcion_id,),
        ).fetchone()
        return int(fila["total_vendido"])

    @staticmethod
    def _validar_cantidad_entradas(cantidad_entradas: int) -> None:
        if not isinstance(cantidad_entradas, int):
            raise VentaError("La cantidad de entradas debe ser un entero.")
        if cantidad_entradas < 1 or cantidad_entradas > 10:
            raise VentaError("La cantidad de entradas debe estar entre 1 y 10.")

    @staticmethod
    def _validar_capacidad_sala(capacidad_sala: int) -> None:
        if not isinstance(capacidad_sala, int):
            raise VentaError("La capacidad de sala debe ser un entero.")
        if capacidad_sala < 20 or capacidad_sala > 300:
            raise VentaError("La capacidad de sala debe estar entre 20 y 300.")

    @staticmethod
    def _validar_precio_unitario(precio_unitario: float) -> None:
        if not isinstance(precio_unitario, (int, float)):
            raise VentaError("El precio unitario debe ser numérico.")
        if precio_unitario <= 0:
            raise VentaError("El precio unitario debe ser mayor que cero.")


if __name__ == "__main__":
    modulo = ModuloVentaEntradas()
    try:
        venta = modulo.vender_entradas(
            funcion_id=1,
            capacidad_sala=100,
            cantidad_entradas=3,
            precio_unitario=15.0,
        )
        print(venta)
        print(modulo.entradas_disponibles(funcion_id=1, capacidad_sala=100))
    finally:
        modulo.cerrar()
