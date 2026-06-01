from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.services.venta_service import VentaError, VentaService
from src.ui.venta_ui import VentaUI


# PE
class PruebasPEVentaEntradas(unittest.TestCase):
	def setUp(self):
		self.tempdir = tempfile.TemporaryDirectory()
		self.ruta = Path(self.tempdir.name) / "ventas.json"
		self.modulo = VentaService(str(self.ruta))

	def tearDown(self):
		self.tempdir.cleanup()

	def test_venta_valida(self):
		# Verifica que una venta normal se registre bien.
		venta = self.modulo.vender_entradas("Hola", 1, (1, 2, 3, 4, 5))
		self.assertEqual(venta.pelicula, "Hola")
		self.assertEqual(venta.funcion_id, 1)
		self.assertEqual(venta.cantidad_entradas, 5)
		self.assertEqual(venta.asientos, (1, 2, 3, 4, 5))
		self.assertEqual(venta.total, 75.0)
		self.assertEqual(venta.estado, "ACTIVA")

	def test_sin_asientos(self):
		# Revisa que no deje comprar sin asientos.
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 1, ())

	def test_mas_de_diez_asientos(self):
		# Comprueba que limite la compra a 10 asientos.
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 1, tuple(range(1, 16)))

	def test_cancelar_venta(self):
		# Confirma que una venta pueda cancelarse.
		venta = self.modulo.vender_entradas("Hola", 1, (1, 2, 3))
		cancelada = self.modulo.cancelar_venta(venta.id_venta)
		self.assertEqual(cancelada.estado, "CANCELADA")

	def test_eliminar_venta(self):
		# Verifica que una venta se pueda eliminar.
		venta = self.modulo.vender_entradas("Hola", 1, (1, 2))
		eliminada = self.modulo.eliminar_venta(venta.id_venta)
		self.assertEqual(eliminada.id_venta, venta.id_venta)

	def test_listar_por_pelicula(self):
		# Revisa que filtre las ventas por pelicula.
		self.modulo.vender_entradas("Hola", 1, (1, 2, 3))
		self.modulo.vender_entradas("Otra", 2, (4, 5))
		ventas = self.modulo.listar_ventas(pelicula="Hola")
		self.assertEqual(len(ventas), 1)
		self.assertEqual(ventas[0].pelicula, "Hola")

	def test_id_autoincrementa(self):
		# Comprueba que el id suba solo en cada venta.
		primera = self.modulo.vender_entradas("Hola", 1, (1,))
		segunda = self.modulo.vender_entradas("Hola", 2, (2,))
		self.assertEqual(primera.id_venta, 1)
		self.assertEqual(segunda.id_venta, 2)


# AVL
class PruebasAVLVentaEntradas(unittest.TestCase):
	def setUp(self):
		self.tempdir = tempfile.TemporaryDirectory()
		self.ruta = Path(self.tempdir.name) / "ventas.json"
		self.modulo = VentaService(str(self.ruta))

	def tearDown(self):
		self.tempdir.cleanup()

	def test_un_asiento(self):
		# Verifica que una compra de un asiento funcione.
		venta = self.modulo.vender_entradas("Hola", 1, (1,))
		self.assertEqual(venta.cantidad_entradas, 1)
		self.assertEqual(venta.total, 15.0)

	def test_nueve_asientos(self):
		# Revisa que una compra de 9 asientos sea valida.
		venta = self.modulo.vender_entradas("Hola", 1, (1, 2, 3, 4, 5, 6, 7, 8, 9))
		self.assertEqual(venta.cantidad_entradas, 9)

	def test_diez_asientos(self):
		# Comprueba que 10 asientos sea el maximo permitido.
		venta = self.modulo.vender_entradas("Hola", 2, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
		self.assertEqual(venta.cantidad_entradas, 10)

	def test_doce_asientos_es_invalido(self):
		# Verifica que mas de 10 asientos no pase.
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 3, tuple(range(1, 12)))

	def test_asiento_ya_usado_en_misma_funcion(self):
		# Comprueba que no repita asientos ocupados.
		self.modulo.vender_entradas("Hola", 1, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 1, (10,))


# Interfaz
class PruebasInterfazVentaEntradas(unittest.TestCase):
	def test_funcion_auto_por_pelicula(self):
		# Revisa que la funcion cambie sola con la pelicula.
		class VariableFalsa:
			def __init__(self, valor=""):
				self.valor = valor

			def get(self):
				return self.valor

			def set(self, valor):
				self.valor = valor

		ui = VentaUI.__new__(VentaUI)
		ui._peliculas_disponibles = ["Pelicula 1", "Pelicula 2"]
		ui._pelicula_var = VariableFalsa("Pelicula 1")
		ui._funcion_var = VariableFalsa("0")
		ui._cargar_ventas = mock.Mock()

		ui._actualizar_funcion_auto()

		self.assertEqual(ui._funcion_var.get(), "1")
		ui._cargar_ventas.assert_called_once_with("Pelicula 1")

	def test_registrar_limpia_asientos(self):
		# Verifica que registrar limpie los asientos seleccionados.
		class VariableFalsa:
			def __init__(self, valor=""):
				self.valor = valor

			def get(self):
				return self.valor

			def set(self, valor):
				self.valor = valor

		class ServicioFalso:
			def __init__(self):
				self.llamadas = []

			def vender_entradas(self, pelicula, funcion_id, asientos_seleccionados):
				self.llamadas.append((pelicula, funcion_id, asientos_seleccionados))
				return object()

			def listar_ventas(self, funcion_id=None, pelicula=None):
				return []

			def asientos_ocupados(self, funcion_id):
				return set()

		ui = VentaUI.__new__(VentaUI)
		ui._root = mock.Mock()
		ui._service = ServicioFalso()
		ui._peliculas_disponibles = ["Pelicula"]
		ui._pelicula_var = VariableFalsa("Pelicula")
		ui._funcion_var = VariableFalsa("1")
		ui._cantidad_var = VariableFalsa("3")
		ui._asientos_var = VariableFalsa("A1, A2, A3")
		ui._asientos_seleccionados = [1, 2, 3]
		ui._cargar_ventas = mock.Mock()
		ui._mantener_ventana_activa = mock.Mock()
		try:
			with mock.patch("src.ui.venta_ui.messagebox.showinfo"), mock.patch("src.ui.venta_ui.messagebox.showerror"):
				ui._registrar()
			self.assertEqual(ui._asientos_seleccionados, [])
			self.assertEqual(ui._asientos_var.get(), "Sin asientos seleccionados")
			self.assertEqual(ui._cantidad_var.get(), "0")
		finally:
			ui._root.destroy.assert_not_called()

	def test_filtrar_por_pelicula(self):
		# Comprueba que la tabla muestre solo la pelicula elegida.
		class VariableFalsa:
			def __init__(self, valor=""):
				self.valor = valor

			def get(self):
				return self.valor

			def set(self, valor):
				self.valor = valor

		class TablaFalsa:
			def __init__(self):
				self.items = ["uno", "dos"]
				self.inserciones = []

			def get_children(self):
				return list(self.items)

			def delete(self, item):
				if item in self.items:
					self.items.remove(item)

			def insert(self, _padre, _posicion, values=None):
				self.inserciones.append(values)

		class ServicioFalso:
			def __init__(self):
				self.ventas = []

			def listar_ventas(self, funcion_id=None, pelicula=None):
				return [venta for venta in self.ventas if pelicula is None or venta.pelicula == pelicula]

			def asientos_ocupados(self, funcion_id):
				return set()

		class VentaFalsa:
			def __init__(self, pelicula):
				self.id_venta = 1
				self.pelicula = pelicula
				self.funcion_id = 1
				self.cantidad_entradas = 2
				self.total = 30.0
				self.fecha_venta = __import__("datetime").datetime.now()
				self.estado = "ACTIVA"

		service = ServicioFalso()
		service.ventas = [VentaFalsa("Hola"), VentaFalsa("Otra")]
		ui = VentaUI.__new__(VentaUI)
		ui._service = service
		ui._tabla = TablaFalsa()
		ui._pelicula_var = VariableFalsa("Hola")

		ui._cargar_ventas("Hola")

		self.assertEqual(len(ui._tabla.inserciones), 1)
		self.assertEqual(ui._tabla.inserciones[0][1], "Hola")


if __name__ == "__main__":
	unittest.main()
