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
        normalizado = Pelicula.normalizar_titulo(pelicula.titulo)
        if self._existe_titulo(peliculas, normalizado):
            raise ValueError("titulo duplicado")
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

    def actualizar(self, titulo, **cambios):
        if "titulo_nuevo" in cambios and "titulo" not in cambios:
            cambios["titulo"] = cambios.pop("titulo_nuevo")
        peliculas = self._leer()
        indice, actual = self._buscar_indice(peliculas, titulo)
        data = {**actual, **cambios}
        data.pop("clasificacion", None)
        nueva = Pelicula(**data)
        actual_norm = Pelicula.normalizar_titulo(actual["titulo"])
        nueva_norm = Pelicula.normalizar_titulo(nueva.titulo)
        if nueva_norm != actual_norm and self._existe_titulo(peliculas, nueva_norm, excluir=indice):
            raise ValueError("titulo duplicado")
        peliculas[indice] = self._a_dict(nueva)
        self._escribir(peliculas)
        return nueva

    def eliminar(self, titulo):
        peliculas = self._leer()
        indice, _ = self._buscar_indice(peliculas, titulo)
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
            return datos
        if isinstance(datos, dict):
            items = datos.get("items")
            if items is None:
                return []
            if not isinstance(items, list):
                raise ValueError("formato de datos invalido")
            return items
        raise ValueError("formato de datos invalido")

    def _escribir(self, peliculas):
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

    def _buscar_indice(self, peliculas, titulo):
        normalizado = Pelicula.normalizar_titulo(titulo)
        for idx, data in enumerate(peliculas):
            if Pelicula.normalizar_titulo(data["titulo"]) == normalizado:
                return idx, data
        raise ValueError("pelicula no encontrada")

    def _existe_titulo(self, peliculas, normalizado, excluir=None):
        for idx, data in enumerate(peliculas):
            if excluir is not None and idx == excluir:
                continue
            if Pelicula.normalizar_titulo(data["titulo"]) == normalizado:
                return True
        return False

    @staticmethod
    def _a_dict(pelicula):
        return {
            "titulo": pelicula.titulo,
            "genero": pelicula.genero,
            "duracion": pelicula.duracion,
        }

    @staticmethod
    def _desde_dict(data):
        return Pelicula(
            titulo=data["titulo"],
            genero=data["genero"],
            duracion=data["duracion"],
        )

    @staticmethod
    def _ruta_por_defecto():
        return Path(__file__).resolve().parent / "peliculas.json"
