from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock
import tkinter as tk


ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from src.services.venta_service import VentaError, VentaService
from src.ui.venta_ui import VentaUI


class PruebasParticionEquivalenciaVentaEntradas(unittest.TestCase):
	def setUp(self):
		self.tempdir = tempfile.TemporaryDirectory()
		self.ruta = Path(self.tempdir.name) / "ventas.json"
		self.modulo = VentaService(str(self.ruta))

	def tearDown(self):
		self.tempdir.cleanup()

	def test_venta_valida_en_clase_equivalencia_valida(self):
		venta = self.modulo.vender_entradas(
			pelicula="Hola",
			funcion_id=1,
			asientos_seleccionados=(1, 2, 3, 4, 5),
		)

		self.assertEqual(venta.pelicula, "Hola")
		self.assertEqual(venta.funcion_id, 1)
		self.assertEqual(venta.cantidad_entradas, 5)
		self.assertEqual(venta.asientos, (1, 2, 3, 4, 5))
		self.assertEqual(venta.total, 75.0)
		self.assertEqual(venta.estado, "ACTIVA")
		self.assertEqual(self.modulo.entradas_disponibles(1), 295)

	def test_cantidad_cero_es_invalida(self):
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas(
				pelicula="Hola",
				funcion_id=1,
				asientos_seleccionados=(),
			)

	def test_cantidad_mayor_a_diez_es_invalida(self):
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas(
				pelicula="Hola",
				funcion_id=1,
				asientos_seleccionados=tuple(range(1, 16)),
			)

	def test_control_de_aforo_rechaza_venta_excedida(self):
		self.modulo.vender_entradas(
			pelicula="Hola",
			funcion_id=1,
			asientos_seleccionados=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
		)

		with self.assertRaises(VentaError):
			self.modulo.vender_entradas(
				pelicula="Hola",
				funcion_id=1,
				asientos_seleccionados=(1, 11),
			)

	def test_cancelar_venta_libera_aforo(self):
		venta = self.modulo.vender_entradas(
			pelicula="Hola",
			funcion_id=1,
			asientos_seleccionados=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
		)
		self.assertEqual(self.modulo.entradas_disponibles(1), 290)

		cancelada = self.modulo.cancelar_venta(venta.id_venta)
		self.assertEqual(cancelada.estado, "CANCELADA")
		self.assertEqual(self.modulo.entradas_disponibles(1), 300)

	def test_eliminar_venta_borra_registro(self):
		venta = self.modulo.vender_entradas(
			pelicula="Hola",
			funcion_id=1,
			asientos_seleccionados=(1, 2),
		)
		eliminada = self.modulo.eliminar_venta(venta.id_venta)
		self.assertEqual(eliminada.id_venta, venta.id_venta)
		self.assertEqual(self.modulo.listar_ventas(), [])

	def test_listar_ventas_por_funcion(self):
		self.modulo.vender_entradas("Hola", 1, (1, 2, 3))
		self.modulo.vender_entradas("Hola", 2, (4, 5, 6, 7))

		ventas_funcion_1 = self.modulo.listar_ventas(1)
		self.assertEqual(len(ventas_funcion_1), 1)
		self.assertEqual(ventas_funcion_1[0].funcion_id, 1)

	def test_listar_ventas_por_pelicula(self):
		self.modulo.vender_entradas("Hola", 1, (1, 2, 3))
		self.modulo.vender_entradas("Otra", 2, (4, 5))

		ventas_hola = self.modulo.listar_ventas(pelicula="Hola")
		self.assertEqual(len(ventas_hola), 1)
		self.assertEqual(ventas_hola[0].pelicula, "Hola")

	def test_limpiar_compras_borra_todos_los_registros(self):
		self.modulo.vender_entradas("Hola", 1, (1, 2, 3))
		self.modulo.vender_entradas("Otra", 2, (4, 5))

		borradas = self.modulo.limpiar_compras()
		self.assertEqual(len(borradas), 2)
		self.assertEqual(self.modulo.listar_ventas(), [])

	def test_id_venta_autoincrementa_desde_uno(self):
		primera = self.modulo.vender_entradas("Hola", 1, (1,))
		segunda = self.modulo.vender_entradas("Hola", 2, (2,))

		self.assertEqual(primera.id_venta, 1)
		self.assertEqual(segunda.id_venta, 2)


class PruebasValoresLimiteVentaEntradas(unittest.TestCase):
	def setUp(self):
		self.tempdir = tempfile.TemporaryDirectory()
		self.ruta = Path(self.tempdir.name) / "ventas.json"
		self.modulo = VentaService(str(self.ruta))

	def tearDown(self):
		self.tempdir.cleanup()

	def test_limite_inferior_cantidad_menos_uno_es_invalido(self):
		with self.assertRaisesRegex(VentaError, "Selecciona al menos un asiento"):
			self.modulo.vender_entradas("Hola", 1, ())

	def test_limite_inferior_cantidad_uno_es_valido(self):
		venta = self.modulo.vender_entradas("Hola", 1, (1,))
		self.assertEqual(venta.cantidad_entradas, 1)
		self.assertEqual(venta.total, 15.0)

	def test_valores_cercanos_al_limite_superior_cantidad(self):
		venta_nueve = self.modulo.vender_entradas("Hola", 1, (1, 2, 3, 4, 5, 6, 7, 8, 9))
		self.assertEqual(venta_nueve.cantidad_entradas, 9)

		venta_diez = self.modulo.vender_entradas("Hola", 2, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
		self.assertEqual(venta_diez.cantidad_entradas, 10)

		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 3, tuple(range(1, 12)))

	def test_aforo_real_en_limite(self):
		self.modulo.vender_entradas("Hola", 1, (1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
		self.modulo.vender_entradas("Hola", 1, (11, 12, 13, 14, 15, 16, 17, 18, 19, 20))

		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 1, (21,))


class PruebasInterfazVentaEntradas(unittest.TestCase):
	def test_funcion_id_se_autocompleta_con_pelicula(self):
		root = tk.Tk()
		root.withdraw()
		tempdir = tempfile.TemporaryDirectory()
		ruta = Path(tempdir.name) / "ventas.json"
		service = VentaService(str(ruta))
		ui = VentaUI(master=root, service=service)
		try:
			if ui._peliculas_disponibles:
				ui._pelicula_var.set(ui._peliculas_disponibles[0])
				ui._actualizar_funcion_auto()
				self.assertEqual(ui._funcion_var.get(), "1")
		finally:
			ui._root.destroy()
			tempdir.cleanup()

	def test_selector_de_asientos_limita_a_diez(self):
		root = tk.Tk()
		root.withdraw()
		tempdir = tempfile.TemporaryDirectory()
		ruta = Path(tempdir.name) / "ventas.json"
		service = VentaService(str(ruta))
		ui = VentaUI(master=root, service=service)
		try:
			for asiento in range(1, 11):
				ui._asientos_seleccionados.append(asiento)
			ui._asientos_var.set(", ".join(f"A{a}" for a in ui._asientos_seleccionados))
			ui._cantidad_var.set(str(len(ui._asientos_seleccionados)))
			self.assertEqual(ui._cantidad_var.get(), "10")
		finally:
			ui._root.destroy()
			tempdir.cleanup()

	@mock.patch("src.ui.venta_ui.messagebox.showinfo")
	@mock.patch("src.ui.venta_ui.messagebox.showerror")
	@mock.patch("src.ui.venta_ui.messagebox.askyesno", return_value=True)
	def test_registrar_envia_los_asientos_seleccionados(self, _askyesno, _showerror, _showinfo):
		class ServicioFalso:
			def __init__(self):
				self.llamadas = []

			def vender_entradas(self, pelicula, funcion_id, asientos_seleccionados):
				self.llamadas.append((pelicula, funcion_id, asientos_seleccionados))
				return object()

			def listar_ventas(self, funcion_id=None):
				return []

			def asientos_ocupados(self, funcion_id):
				return set()

		root = tk.Tk()
		root.withdraw()
		service = ServicioFalso()
		ui = VentaUI(master=root, service=service)
		try:
			ui._pelicula_var.set(ui._peliculas_disponibles[0] if ui._peliculas_disponibles else "Pelicula")
			ui._funcion_var.set("1")
			ui._asientos_seleccionados = [1, 2, 3]
			ui._asientos_var.set("A1, A2, A3")
			ui._cantidad_var.set("3")
			ui._registrar()
			self.assertEqual(service.llamadas, [(ui._pelicula_var.get(), 1, (1, 2, 3))])
			self.assertEqual(ui._pelicula_var.get(), ui._peliculas_disponibles[0] if ui._peliculas_disponibles else "Pelicula")
			self.assertEqual(ui._funcion_var.get(), "1")
			self.assertEqual(ui._cantidad_var.get(), "0")
			self.assertEqual(ui._asientos_var.get(), "Sin asientos seleccionados")
			self.assertEqual(ui._asientos_seleccionados, [])
		finally:
			ui._root.destroy()

	@mock.patch("src.ui.venta_ui.messagebox.showinfo")
	@mock.patch("src.ui.venta_ui.messagebox.showerror")
	def test_cargar_ventas_filtra_por_pelicula(self, _showerror, _showinfo):
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
			filas = ui._tabla.get_children()
			self.assertEqual(len(filas), 1)
			valores = ui._tabla.item(filas[0], "values")
			self.assertEqual(valores[1], "Hola")
		finally:
			ui._root.destroy()


if __name__ == "__main__":
	unittest.main()