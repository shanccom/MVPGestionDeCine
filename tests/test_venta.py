from pathlib import Path
import sys
import tempfile
import unittest
import tkinter as tk


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.append(str(SRC))

from services.venta_service import VentaError, VentaService
from ui.venta_ui import VentaUI


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
			capacidad_sala=100,
			cantidad_entradas=5,
		)

		self.assertEqual(venta.pelicula, "Hola")
		self.assertEqual(venta.funcion_id, 1)
		self.assertEqual(venta.cantidad_entradas, 5)
		self.assertEqual(venta.total, 75.0)
		self.assertEqual(venta.estado, "ACTIVA")
		self.assertEqual(self.modulo.entradas_disponibles(1, 100), 95)

	def test_cantidad_cero_es_invalida(self):
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas(
				pelicula="Hola",
				funcion_id=1,
				capacidad_sala=100,
				cantidad_entradas=0,
			)

	def test_cantidad_mayor_a_diez_es_invalida(self):
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas(
				pelicula="Hola",
				funcion_id=1,
				capacidad_sala=100,
				cantidad_entradas=15,
			)

	def test_capacidad_fuera_de_rango_es_invalida(self):
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas(
				pelicula="Hola",
				funcion_id=1,
				capacidad_sala=10,
				cantidad_entradas=1,
			)

		with self.assertRaises(VentaError):
			self.modulo.vender_entradas(
				pelicula="Hola",
				funcion_id=1,
				capacidad_sala=500,
				cantidad_entradas=1,
			)

	def test_control_de_aforo_rechaza_venta_excedida(self):
		self.modulo.vender_entradas(
			pelicula="Hola",
			funcion_id=1,
			capacidad_sala=100,
			cantidad_entradas=98,
		)

		with self.assertRaises(VentaError):
			self.modulo.vender_entradas(
				pelicula="Hola",
				funcion_id=1,
				capacidad_sala=100,
				cantidad_entradas=5,
			)

	def test_cancelar_venta_libera_aforo(self):
		venta = self.modulo.vender_entradas(
			pelicula="Hola",
			funcion_id=1,
			capacidad_sala=100,
			cantidad_entradas=40,
		)
		self.assertEqual(self.modulo.entradas_disponibles(1, 100), 60)

		cancelada = self.modulo.cancelar_venta(venta.id)
		self.assertEqual(cancelada.estado, "CANCELADA")
		self.assertEqual(self.modulo.entradas_disponibles(1, 100), 100)

	def test_listar_ventas_por_funcion(self):
		self.modulo.vender_entradas("Hola", 1, 100, 3)
		self.modulo.vender_entradas("Hola", 2, 100, 4)

		ventas_funcion_1 = self.modulo.listar_ventas(1)
		self.assertEqual(len(ventas_funcion_1), 1)
		self.assertEqual(ventas_funcion_1[0].funcion_id, 1)

	def test_id_venta_autoincrementa_desde_uno(self):
		primera = self.modulo.vender_entradas("Hola", 1, 100, 1)
		segunda = self.modulo.vender_entradas("Hola", 2, 100, 1)

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
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 1, 100, 0)

	def test_limite_inferior_cantidad_uno_es_valido(self):
		venta = self.modulo.vender_entradas("Hola", 1, 100, 1)
		self.assertEqual(venta.cantidad_entradas, 1)
		self.assertEqual(venta.total, 15.0)

	def test_valores_cercanos_al_limite_superior_cantidad(self):
		venta_nueve = self.modulo.vender_entradas("Hola", 1, 100, 9)
		self.assertEqual(venta_nueve.cantidad_entradas, 9)

		venta_diez = self.modulo.vender_entradas("Hola", 2, 100, 10)
		self.assertEqual(venta_diez.cantidad_entradas, 10)

		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 3, 100, 11)

	def test_limite_inferior_capacidad_diecinueve_es_invalido(self):
		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 1, 19, 1)

	def test_limite_inferior_capacidad_veinte_es_valido(self):
		venta = self.modulo.vender_entradas("Hola", 1, 20, 1)
		self.assertEqual(venta.cantidad_entradas, 1)

	def test_valores_cercanos_al_limite_superior_capacidad(self):
		venta_299 = self.modulo.vender_entradas("Hola", 1, 299, 10)
		self.assertEqual(venta_299.cantidad_entradas, 10)

		venta_300 = self.modulo.vender_entradas("Hola", 2, 300, 10)
		self.assertEqual(venta_300.cantidad_entradas, 10)

		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 3, 301, 1)

	def test_aforo_real_en_limite(self):
		self.modulo.vender_entradas("Hola", 1, 20, 10)
		self.modulo.vender_entradas("Hola", 1, 20, 10)

		with self.assertRaises(VentaError):
			self.modulo.vender_entradas("Hola", 1, 20, 1)


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


if __name__ == "__main__":
	unittest.main()