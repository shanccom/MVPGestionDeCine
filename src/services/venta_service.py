from __future__ import annotations

from models.venta import Venta
from storage.ventas.venta_repository import VentaRepository


class VentaError(ValueError):
	pass


class VentaService:
	PRECIO_UNITARIO = 15.0

	def __init__(self, ruta=None, repository=None):
		self._repo = repository or VentaRepository(ruta)

	def vender_entradas(self, pelicula, funcion_id, asientos_seleccionados, capacidad_sala=300):
		try:
			if not isinstance(asientos_seleccionados, (list, tuple)):
				raise VentaError("Los asientos deben ser una lista o tupla de numeros enteros.")
			cantidad_entradas = len(asientos_seleccionados)
			if cantidad_entradas > 10:
				raise VentaError("No se puede comprar mas de 10 asientos.")
			if cantidad_entradas == 0:
				raise VentaError("Selecciona al menos un asiento.")
			ocupados = self._repo.asientos_ocupados(funcion_id)
			conflictivos = sorted(set(asientos_seleccionados).intersection(ocupados))
			if conflictivos:
				raise VentaError("Uno o mas de los asientos seleccionados ya fueron comprados.")
			venta = Venta(
				id_venta=None,
				pelicula=pelicula,
				funcion_id=funcion_id,
				asientos=tuple(asientos_seleccionados),
				cantidad_entradas=cantidad_entradas,
				total=round(cantidad_entradas * self.PRECIO_UNITARIO, 2),
			)
			if capacidad_sala is not None:
				self._validar_capacidad_sala(capacidad_sala)
				entradas_disponibles = capacidad_sala - self._repo.total_entradas_activas(funcion_id)
				if venta.cantidad_entradas > entradas_disponibles:
					raise VentaError("No se puede registrar la venta: se excede la capacidad disponible.")
			return self._repo.guardar(venta)
		except ValueError as exc:
			if isinstance(exc, VentaError):
				raise
			raise VentaError(str(exc)) from exc

	def cancelar_venta(self, venta_id):
		try:
			return self._repo.cancelar(venta_id)
		except ValueError as exc:
			raise VentaError(str(exc)) from exc

	def listar_ventas(self, funcion_id=None, pelicula=None):
		ventas = self._repo.listar(funcion_id)
		if pelicula is None:
			return ventas
		return [venta for venta in ventas if venta.pelicula == pelicula]

	def asientos_ocupados(self, funcion_id):
		return self._repo.asientos_ocupados(funcion_id)

	def limpiar_compras(self):
		return self._repo.limpiar()

	def eliminar_venta(self, venta_id):
		try:
			return self._repo.eliminar(venta_id)
		except ValueError as exc:
			raise VentaError(str(exc)) from exc

	def entradas_disponibles(self, funcion_id, capacidad_sala=300):
		if capacidad_sala is None:
			return None
		self._validar_capacidad_sala(capacidad_sala)
		return capacidad_sala - self._repo.total_entradas_activas(funcion_id)

	@staticmethod
	def _validar_capacidad_sala(capacidad_sala):
		if not isinstance(capacidad_sala, int) or isinstance(capacidad_sala, bool):
			raise VentaError("La capacidad de sala debe ser un entero.")
		if capacidad_sala < 20 or capacidad_sala > 300:
			raise VentaError("La capacidad de sala debe estar entre 20 y 300.")