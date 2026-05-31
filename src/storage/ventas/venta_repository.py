from __future__ import annotations

import json
from pathlib import Path

from models.venta import Venta


class VentaRepository:
    def __init__(self, ruta=None):
        self._ruta = Path(ruta) if ruta else self._ruta_por_defecto()
        self._asegurar_archivo()

    def guardar(self, venta):
        if not isinstance(venta, Venta):
            raise ValueError("venta invalida")
        ventas = self._leer()
        data = venta.to_dict()
        data["id_venta"] = self._siguiente_id(ventas)
        ventas.append(data)
        self._escribir(ventas)
        return self._desde_dict(data)

    def listar(self, funcion_id=None):
        ventas = self._leer()
        if funcion_id is None:
            return [self._desde_dict(data) for data in ventas]
        return [
            self._desde_dict(data)
            for data in ventas
            if data.get("funcion_id") == funcion_id
        ]

    def buscar_por_id(self, venta_id):
        for data in self._leer():
            if data.get("id_venta") == venta_id:
                return self._desde_dict(data)
        raise ValueError("venta no encontrada")

    def cancelar(self, venta_id):
        ventas = self._leer()
        for indice, data in enumerate(ventas):
            if data.get("id_venta") == venta_id:
                if data.get("estado") == "CANCELADA":
                    raise ValueError("venta ya cancelada")
                data["estado"] = "CANCELADA"
                ventas[indice] = data
                self._escribir(ventas)
                return self._desde_dict(data)
        raise ValueError("venta no encontrada")

    def eliminar(self, venta_id):
        ventas = self._leer()
        for indice, data in enumerate(ventas):
            if data.get("id_venta") == venta_id:
                eliminada = ventas.pop(indice)
                self._escribir(ventas)
                return self._desde_dict(eliminada)
        raise ValueError("venta no encontrada")

    def total_entradas_activas(self, funcion_id):
        return sum(
            data["cantidad_entradas"]
            for data in self._leer()
            if data.get("funcion_id") == funcion_id and data.get("estado") == "ACTIVA"
        )

    def asientos_ocupados(self, funcion_id):
        ocupados = set()
        for data in self._leer():
            if data.get("funcion_id") != funcion_id:
                continue
            if data.get("estado") != "ACTIVA":
                continue
            for asiento in data.get("asientos", []):
                ocupados.add(asiento)
        return ocupados

    def _asegurar_archivo(self):
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        if not self._ruta.exists():
            self._ruta.write_text(
                json.dumps(self._plantilla(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def _leer(self):
        datos = self._leer_raw()
        if isinstance(datos, dict):
            items = datos.get("items")
            if items is None:
                return []
            if not isinstance(items, list):
                raise ValueError("formato de datos invalido")
            return items
        if isinstance(datos, list):
            return datos
        raise ValueError("formato de datos invalido")

    def _escribir(self, ventas):
        datos = self._leer_raw()
        if isinstance(datos, dict):
            comentario = datos.get("comentario", "Datos de ventas")
            payload = {"comentario": comentario, "items": ventas}
        else:
            payload = ventas
        self._ruta.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _leer_raw(self):
        contenido = self._ruta.read_text(encoding="utf-8").strip()
        if not contenido:
            return self._plantilla()
        return json.loads(contenido)

    @staticmethod
    def _plantilla():
        return {"comentario": "Datos de ventas", "items": []}

    @staticmethod
    def _siguiente_id(ventas):
        if not ventas:
            return 1
        return max(data.get("id_venta", 0) for data in ventas) + 1

    @staticmethod
    def _desde_dict(data):
        return Venta.from_dict(data)

    @staticmethod
    def _ruta_por_defecto():
        return Path(__file__).resolve().parent / "ventas.json"