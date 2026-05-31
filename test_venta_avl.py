import os
import tempfile
import unittest

from modulo_venta_entradas import ModuloVentaEntradas, VentaError


class PruebasValoresLimiteVentaEntradas(unittest.TestCase):
    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile(delete=False)
        self.tempfile.close()
        self.modulo = ModuloVentaEntradas(self.tempfile.name)

    def tearDown(self):
        self.modulo.cerrar()
        if os.path.exists(self.tempfile.name):
            os.remove(self.tempfile.name)

    def test_limite_inferior_cantidad_menos_uno_es_invalido(self):
        with self.assertRaises(VentaError):
            self.modulo.vender_entradas(1, 100, 0, 15.0)

    def test_limite_inferior_cantidad_uno_es_valido(self):
        venta = self.modulo.vender_entradas(1, 100, 1, 15.0)
        self.assertEqual(venta.cantidad_entradas, 1)
        self.assertEqual(venta.total, 15.0)

    def test_valores_cercanos_al_limite_superior_cantidad(self):
        venta_nueve = self.modulo.vender_entradas(1, 100, 9, 15.0)
        self.assertEqual(venta_nueve.cantidad_entradas, 9)

        venta_diez = self.modulo.vender_entradas(2, 100, 10, 15.0)
        self.assertEqual(venta_diez.cantidad_entradas, 10)

        with self.assertRaises(VentaError):
            self.modulo.vender_entradas(3, 100, 11, 15.0)

    def test_limite_inferior_capacidad_diecinueve_es_invalido(self):
        with self.assertRaises(VentaError):
            self.modulo.vender_entradas(1, 19, 1, 15.0)

    def test_limite_inferior_capacidad_veinte_es_valido(self):
        venta = self.modulo.vender_entradas(1, 20, 1, 15.0)
        self.assertEqual(venta.cantidad_entradas, 1)

    def test_valores_cercanos_al_limite_superior_capacidad(self):
        venta_299 = self.modulo.vender_entradas(1, 299, 10, 15.0)
        self.assertEqual(venta_299.cantidad_entradas, 10)

        venta_300 = self.modulo.vender_entradas(2, 300, 10, 15.0)
        self.assertEqual(venta_300.cantidad_entradas, 10)

        with self.assertRaises(VentaError):
            self.modulo.vender_entradas(3, 301, 1, 15.0)

    def test_aforo_real_en_limite(self):
        self.modulo.vender_entradas(1, 20, 10, 15.0)
        self.modulo.vender_entradas(1, 20, 10, 15.0)

        with self.assertRaises(VentaError):
            self.modulo.vender_entradas(1, 20, 1, 15.0)


if __name__ == "__main__":
    unittest.main()
