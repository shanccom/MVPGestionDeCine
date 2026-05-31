import json
from pathlib import Path

from models.pelicula import Pelicula

class PeliculaRepository:
    def __init__(self, ruta=None):
        self._ruta = Path(ruta) if ruta else self._ruta_por_defecto()
        self._asegurar_archivo()

    def guardar(self, pelicula):
        if not isinstance(pelicula, Pelicula):
            raise ValueError("pelicula invalida")
        peliculas = self._leer()
        if pelicula.id_pelicula is None:
            pelicula.asignar_id(self._siguiente_id(peliculas))
        elif self._existe_id(peliculas, pelicula.id_pelicula):
            raise ValueError("id_pelicula duplicado")
        peliculas.append(self._a_dict(pelicula))
        self._escribir(peliculas)
        return pelicula

    def listar(self):
        return [self._desde_dict(data) for data in self._leer()]

    def buscar_por_titulo(self, titulo):
        normalizado = Pelicula.normalizar_titulo(titulo)
        for data in self._leer():
            if Pelicula.normalizar_titulo(data["titulo"]) == normalizado:
                return self._desde_dict(data)
        raise ValueError("pelicula no encontrada")

    def buscar_por_id(self, id_pelicula):
        for data in self._leer():
            if data.get("id_pelicula") == id_pelicula:
                return self._desde_dict(data)
        raise ValueError("pelicula no encontrada")

    def actualizar(self, id_pelicula, **cambios):
        if "titulo_nuevo" in cambios and "titulo" not in cambios:
            cambios["titulo"] = cambios.pop("titulo_nuevo")
        peliculas = self._leer()
        indice, actual = self._buscar_indice(peliculas, id_pelicula)
        data = {**actual, **cambios}
        data["id_pelicula"] = actual.get("id_pelicula")
        data.pop("clasificacion", None)
        nueva = Pelicula(**data)
        peliculas[indice] = self._a_dict(nueva)
        self._escribir(peliculas)
        return nueva

    def eliminar(self, id_pelicula):
        peliculas = self._leer()
        indice, _ = self._buscar_indice(peliculas, id_pelicula)
        peliculas.pop(indice)
        self._escribir(peliculas)

    def _asegurar_archivo(self):
        self._ruta.parent.mkdir(parents=True, exist_ok=True)
        if not self._ruta.exists():
            self._ruta.write_text(
                json.dumps(self._plantilla(), ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

    def _leer(self):
        datos = self._leer_raw()
        if isinstance(datos, list):
            peliculas, actualizado = self._normalizar_items(datos)
            if actualizado:
                self._escribir(peliculas, datos)
            return peliculas
        if isinstance(datos, dict):
            items = datos.get("items")
            if items is None:
                return []
            if not isinstance(items, list):
                raise ValueError("formato de datos invalido")
            peliculas, actualizado = self._normalizar_items(items)
            if actualizado:
                self._escribir(peliculas, datos)
            return peliculas
        raise ValueError("formato de datos invalido")

    def _escribir(self, peliculas, datos=None):
        if datos is None:
            datos = self._leer_raw()
        if isinstance(datos, dict):
            comentario = datos.get("comentario", "Datos de peliculas")
            payload = {"comentario": comentario, "items": peliculas}
        else:
            payload = peliculas
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
        return {"comentario": "Datos de peliculas", "items": []}

    def _buscar_indice(self, peliculas, id_pelicula):
        for idx, data in enumerate(peliculas):
            if data.get("id_pelicula") == id_pelicula:
                return idx, data
        raise ValueError("pelicula no encontrada")

    def _existe_id(self, peliculas, id_pelicula):
        return any(data.get("id_pelicula") == id_pelicula for data in peliculas)

    def _siguiente_id(self, peliculas):
        max_id = 0
        for data in peliculas:
            valor = data.get("id_pelicula")
            if isinstance(valor, int) and not isinstance(valor, bool):
                max_id = max(max_id, valor)
        return max_id + 1

    def _normalizar_items(self, items):
        actualizado = False
        max_id = 0
        for data in items:
            if not isinstance(data, dict):
                raise ValueError("formato de datos invalido")
            valor = data.get("id_pelicula")
            if isinstance(valor, int) and not isinstance(valor, bool) and valor > 0:
                max_id = max(max_id, valor)
        siguiente = max_id + 1
        for data in items:
            valor = data.get("id_pelicula")
            if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
                data["id_pelicula"] = siguiente
                siguiente += 1
                actualizado = True
            if "clasificacion" in data:
                data.pop("clasificacion", None)
                actualizado = True
        return items, actualizado

    @staticmethod
    def _a_dict(pelicula):
        return {
            "id_pelicula": pelicula.id_pelicula,
            "titulo": pelicula.titulo,
            "genero": pelicula.genero,
            "duracion": pelicula.duracion,
        }

    @staticmethod
    def _desde_dict(data):
        return Pelicula(
            id_pelicula=data.get("id_pelicula"),
            titulo=data["titulo"],
            genero=data["genero"],
            duracion=data["duracion"],
        )

    @staticmethod
    def _ruta_por_defecto():
        return Path(__file__).resolve().parent / "peliculas.json"
