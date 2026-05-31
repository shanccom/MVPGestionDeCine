import json
from pathlib import Path

from models.funcion import Funcion


class FuncionRepository:
    def __init__(self, ruta=None):
        self._ruta = Path(ruta) if ruta else self._ruta_por_defecto()
        self._asegurar_archivo()

    def guardar(self, funcion):
        if not isinstance(funcion, Funcion):
            raise ValueError("funcion invalida")
        funciones = self._leer()
        if funcion.id_funcion is None:
            funcion.asignar_id(self._siguiente_id(funciones))
        elif self._existe_id(funciones, funcion.id_funcion):
            raise ValueError("id_funcion duplicado")
        funciones.append(self._a_dict(funcion))
        self._escribir(funciones)
        return funcion

    def listar(self):
        return [self._desde_dict(data) for data in self._leer()]

    def buscar_por_id(self, id_funcion):
        for data in self._leer():
            if data.get("id_funcion") == id_funcion:
                return self._desde_dict(data)
        raise ValueError("funcion no encontrada")

    def actualizar(self, id_funcion, **cambios):
        funciones = self._leer()
        indice, actual = self._buscar_indice(funciones, id_funcion)
        data = {**actual, **cambios}
        data["id_funcion"] = actual.get("id_funcion")
        nueva = Funcion.from_dict(data)
        funciones[indice] = self._a_dict(nueva)
        self._escribir(funciones)
        return nueva

    def eliminar(self, id_funcion):
        funciones = self._leer()
        indice, eliminada = self._buscar_indice(funciones, id_funcion)
        funciones.pop(indice)
        self._escribir(funciones)
        return self._desde_dict(eliminada)

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
            funciones, actualizado = self._normalizar_items(items)
            if actualizado:
                self._escribir(funciones, datos)
            return funciones
        if isinstance(datos, list):
            funciones, actualizado = self._normalizar_items(datos)
            if actualizado:
                self._escribir(funciones, datos)
            return funciones
        raise ValueError("formato de datos invalido")

    def _escribir(self, funciones, datos=None):
        if datos is None:
            datos = self._leer_raw()
        if isinstance(datos, dict):
            comentario = datos.get("comentario", "Datos de funciones")
            payload = {"comentario": comentario, "items": funciones}
        else:
            payload = funciones
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
        return {"comentario": "Datos de funciones", "items": []}

    def _buscar_indice(self, funciones, id_funcion):
        for idx, data in enumerate(funciones):
            if data.get("id_funcion") == id_funcion:
                return idx, data
        raise ValueError("funcion no encontrada")

    @staticmethod
    def _existe_id(funciones, id_funcion):
        return any(data.get("id_funcion") == id_funcion for data in funciones)

    @staticmethod
    def _siguiente_id(funciones):
        max_id = 0
        for data in funciones:
            valor = data.get("id_funcion")
            if isinstance(valor, int) and not isinstance(valor, bool):
                max_id = max(max_id, valor)
        return max_id + 1

    def _normalizar_items(self, items):
        actualizado = False
        max_id = 0
        for data in items:
            if not isinstance(data, dict):
                raise ValueError("formato de datos invalido")
            valor = data.get("id_funcion")
            if isinstance(valor, int) and not isinstance(valor, bool) and valor > 0:
                max_id = max(max_id, valor)
        siguiente = max_id + 1
        for data in items:
            valor = data.get("id_funcion")
            if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
                data["id_funcion"] = siguiente
                siguiente += 1
                actualizado = True
        return items, actualizado

    @staticmethod
    def _a_dict(funcion):
        return funcion.to_dict()

    @staticmethod
    def _desde_dict(data):
        return Funcion.from_dict(data)

    @staticmethod
    def _ruta_por_defecto():
        return Path(__file__).resolve().parent / "funciones.json"
