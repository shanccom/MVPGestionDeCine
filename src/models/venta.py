from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Venta:
	id_venta: int | None
	pelicula: str
	funcion_id: int
	cantidad_entradas: int
	total: float
	fecha_venta: datetime | None = None
	estado: str = "ACTIVA"

	CANTIDAD_MIN = 1
	CANTIDAD_MAX = 10
	ESTADOS_VALIDOS = {"ACTIVA", "CANCELADA"}

	def __post_init__(self):
		self.id_venta = self._validar_id(self.id_venta)
		self.pelicula = self._validar_texto(self.pelicula, "pelicula")
		self.funcion_id = self._validar_id(self.funcion_id, nombre="funcion_id")
		self.cantidad_entradas = self._validar_cantidad(self.cantidad_entradas)
		self.total = self._validar_total(self.total)
		self.estado = self._validar_estado(self.estado)
		if self.fecha_venta is None:
			self.fecha_venta = datetime.now()
		elif not isinstance(self.fecha_venta, datetime):
			raise ValueError("fecha_venta invalida")

	def to_dict(self):
		return {
			"id_venta": self.id_venta,
			"pelicula": self.pelicula,
			"funcion_id": self.funcion_id,
			"cantidad_entradas": self.cantidad_entradas,
			"total": self.total,
			"fecha_venta": self.fecha_venta.isoformat(timespec="seconds"),
			"estado": self.estado,
		}

	@classmethod
	def from_dict(cls, data):
		fecha = data.get("fecha_venta")
		if isinstance(fecha, str) and fecha:
			fecha = datetime.fromisoformat(fecha)
		else:
			fecha = None
		return cls(
			id_venta=data.get("id_venta"),
			pelicula=data.get("pelicula", "Sin pelicula"),
			funcion_id=data["funcion_id"],
			cantidad_entradas=data["cantidad_entradas"],
			total=data["total"],
			fecha_venta=fecha,
			estado=data.get("estado", "ACTIVA"),
		)

	@staticmethod
	def _validar_id(valor, nombre="id_venta"):
		if valor is None:
			return None
		if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
			raise ValueError(f"{nombre} invalido")
		return valor

	@staticmethod
	def _validar_texto(valor, nombre):
		if not isinstance(valor, str):
			raise ValueError(f"{nombre} invalido")
		valor = valor.strip()
		if not valor:
			raise ValueError(f"{nombre} requerido")
		return valor

	@classmethod
	def _validar_cantidad(cls, valor):
		if not isinstance(valor, int) or isinstance(valor, bool):
			raise ValueError("cantidad de entradas invalida")
		if valor < cls.CANTIDAD_MIN or valor > cls.CANTIDAD_MAX:
			raise ValueError("cantidad de entradas fuera de rango")
		return valor

	@staticmethod
	def _validar_total(valor):
		if not isinstance(valor, (int, float)) or isinstance(valor, bool):
			raise ValueError("total invalido")
		if valor <= 0:
			raise ValueError("total fuera de rango")
		return round(float(valor), 2)

	@classmethod
	def _validar_estado(cls, valor):
		if not isinstance(valor, str):
			raise ValueError("estado invalido")
		valor = valor.strip().upper()
		if valor not in cls.ESTADOS_VALIDOS:
			raise ValueError("estado invalido")
		return valor