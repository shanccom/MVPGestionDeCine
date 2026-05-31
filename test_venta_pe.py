import os
import tempfile
import unittest

from modulo_venta_entradas import ModuloVentaEntradas, VentaError


class PruebasParticionEquivalenciaVentaEntradas(unittest.TestCase):
    def setUp(self):
        self.tempfile = tempfile.NamedTemporaryFile(delete=False)
        self.tempfile.close()
        self.modulo = ModuloVentaEntradas(self.tempfile.name)

    def tearDown(self):
        self.modulo.cerrar()
        if os.path.exists(self.tempfile.name):
            os.remove(self.tempfile.name)

    def test_venta_valida_en_clase_equivalencia_valida(self):
        venta = self.modulo.vender_entradas(
            funcion_id=1,
            capacidad_sala=100,
            cantidad_entradas=5,
            precio_unitario=15.0,
        )

        self.assertEqual(venta.funcion_id, 1)
        self.assertEqual(venta.cantidad_entradas, 5)
        self.assertEqual(venta.total, 75.0)
        self.assertEqual(venta.estado, "ACTIVA")
        self.assertEqual(self.modulo.entradas_disponibles(1, 100), 95)

    def test_cantidad_cero_es_invalida(self):
        with self.assertRaises(VentaError):
            self.modulo.vender_entradas(
                funcion_id=1,
                capacidad_sala=100,
                cantidad_entradas=0,
                precio_unitario=15.0,
            )

    def test_cantidad_mayor_a_diez_es_invalida(self):
        with self.assertRaises(VentaError):
            self.modulo.vender_entradas(
                funcion_id=1,
                capacidad_sala=100,
                cantidad_entradas=15,
                precio_unitario=15.0,
            )

    def test_capacidad_fuera_de_rango_es_invalida(self):
        with self.assertRaises(VentaError):
            self.modulo.vender_entradas(
                funcion_id=1,
                capacidad_sala=10,
                cantidad_entradas=1,
                precio_unitario=15.0,
            )

        with self.assertRaises(VentaError):
            self.modulo.vender_entradas(
                funcion_id=1,
                capacidad_sala=500,
                cantidad_entradas=1,
                precio_unitario=15.0,
            )

    def test_control_de_aforo_rechaza_venta_excedida(self):
        self.modulo.vender_entradas(
            funcion_id=1,
            capacidad_sala=100,
            cantidad_entradas=98,
            precio_unitario=15.0,
        )

        with self.assertRaises(VentaError):
            self.modulo.vender_entradas(
                funcion_id=1,
                capacidad_sala=100,
                cantidad_entradas=5,
                precio_unitario=15.0,
            )

    def test_cancelar_venta_libera_aforo(self):
        venta = self.modulo.vender_entradas(
            funcion_id=1,
            capacidad_sala=100,
            cantidad_entradas=40,
            precio_unitario=15.0,
        )
        self.assertEqual(self.modulo.entradas_disponibles(1, 100), 60)

        cancelada = self.modulo.cancelar_venta(venta.id)
        self.assertEqual(cancelada.estado, "CANCELADA")
        self.assertEqual(self.modulo.entradas_disponibles(1, 100), 100)

    def test_listar_ventas_por_funcion(self):
        self.modulo.vender_entradas(1, 100, 3, 15.0)
        self.modulo.vender_entradas(2, 100, 4, 15.0)

        ventas_funcion_1 = self.modulo.listar_ventas(1)
        self.assertEqual(len(ventas_funcion_1), 1)
        self.assertEqual(ventas_funcion_1[0].funcion_id, 1)


if __name__ == "__main__":
    unittest.main()
