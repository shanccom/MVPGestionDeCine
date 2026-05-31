from pathlib import Path
import sys
import tempfile
import tkinter as tk
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
		venta = self.modulo.vender_entradas("Hola", 1, (1, 2, 3, 4, 5))
		self.assertEqual(venta.pelicula, "Hola")
		self.assertEqual(venta.funcion_id, 1)
		self.assertEqual(venta.cantidad_entradas, 5)
		self.assertEqual(venta.asientos, (1, 2, 3, 4, 5))
		self.assertEqual(venta.total, 75.0)
		self.assertEqual(venta.estado, "ACTIVA")

	def test_sin_asientos(self):
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 1, ())

	def test_mas_de_diez_asientos(self):
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 1, tuple(range(1, 16)))

	def test_cancelar_venta(self):
		venta = self.modulo.vender_entradas("Hola", 1, (1, 2, 3))
		cancelada = self.modulo.cancelar_venta(venta.id_venta)
		self.assertEqual(cancelada.estado, "CANCELADA")

	def test_eliminar_venta(self):
		venta = self.modulo.vender_entradas("Hola", 1, (1, 2))
		eliminada = self.modulo.eliminar_venta(venta.id_venta)
		self.assertEqual(eliminada.id_venta, venta.id_venta)

	def test_listar_por_pelicula(self):
		self.modulo.vender_entradas("Hola", 1, (1, 2, 3))
		self.modulo.vender_entradas("Otra", 2, (4, 5))
		ventas = self.modulo.listar_ventas(pelicula="Hola")
		self.assertEqual(len(ventas), 1)
		self.assertEqual(ventas[0].pelicula, "Hola")

	def test_id_autoincrementa(self):
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
		venta = self.modulo.vender_entradas("Hola", 1, (1,))
		self.assertEqual(venta.cantidad_entradas, 1)
		self.assertEqual(venta.total, 15.0)

	def test_nueve_asientos(self):
		venta = self.modulo.vender_entradas("Hola", 1, (1, 2, 3, 4, 5, 6, 7, 8, 9))
		self.assertEqual(venta.cantidad_entradas, 9)

	def test_diez_asientos(self):
		venta = self.modulo.vender_entradas("Hola", 2, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
		self.assertEqual(venta.cantidad_entradas, 10)

	def test_doce_asientos_es_invalido(self):
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 3, tuple(range(1, 12)))

	def test_asiento_ya_usado_en_misma_funcion(self):
		self.modulo.vender_entradas("Hola", 1, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 1, (10,))


# Interfaz
class PruebasInterfazVentaEntradas(unittest.TestCase):
	def crear_ui(self):
		try:
			root = tk.Tk()
		except tk.TclError:
			self.skipTest("Tk no disponible")

		root.withdraw()
		tempdir = tempfile.TemporaryDirectory()
		ruta = Path(tempdir.name) / "ventas.json"
		service = VentaService(str(ruta))
		ui = VentaUI(master=root, service=service)
		return root, tempdir, ui

	def test_funcion_auto_por_pelicula(self):
		root, tempdir, ui = self.crear_ui()
		try:
			if ui._peliculas_disponibles:
				ui._pelicula_var.set(ui._peliculas_disponibles[0])
				ui._actualizar_funcion_auto()
				self.assertEqual(ui._funcion_var.get(), "1")
		finally:
			ui._root.destroy()
			tempdir.cleanup()

	def test_registrar_limpia_asientos(self):
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

		root = tk.Tk()
		root.withdraw()
		ui = VentaUI(master=root, service=ServicioFalso())
		try:
			ui._pelicula_var.set(ui._peliculas_disponibles[0] if ui._peliculas_disponibles else "Pelicula")
			ui._funcion_var.set("1")
			ui._asientos_seleccionados = [1, 2, 3]
			ui._asientos_var.set("A1, A2, A3")
			ui._cantidad_var.set("3")
			with mock.patch("src.ui.venta_ui.messagebox.showinfo"), mock.patch("src.ui.venta_ui.messagebox.showerror"):
				ui._registrar()
			self.assertEqual(ui._asientos_seleccionados, [])
			self.assertEqual(ui._asientos_var.get(), "Sin asientos seleccionados")
			self.assertEqual(ui._cantidad_var.get(), "0")
		finally:
			ui._root.destroy()

	def test_filtrar_por_pelicula(self):
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

		root = tk.Tk()
		root.withdraw()
		service = ServicioFalso()
		service.ventas = [VentaFalsa("Hola"), VentaFalsa("Otra")]
		ui = VentaUI(master=root, service=service)
		try:
			ui._cargar_ventas("Hola")
			self.assertEqual(len(ui._tabla.get_children()), 1)
		finally:
			ui._root.destroy()


if __name__ == "__main__":
	unittest.main()
