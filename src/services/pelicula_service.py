from models.pelicula import Pelicula


class PeliculaService:
    def __init__(self):
        self._peliculas = []
        self._funciones_asociadas = set()

    def registrar(self, titulo, genero, duracion):
        pelicula = Pelicula(
            titulo=titulo,
            genero=genero,
            duracion=duracion,
        )
        normalizado = Pelicula.normalizar_titulo(pelicula.titulo)
        if self._existe_titulo(normalizado):
            raise ValueError("titulo duplicado")
        self._peliculas.append(pelicula)
        return pelicula

    def listar(self):
        return list(self._peliculas)

    def actualizar(self, titulo, **cambios):
        indice, pelicula = self._buscar_por_titulo(titulo)
        data = {
            "titulo": pelicula.titulo,
            "genero": pelicula.genero,
            "duracion": pelicula.duracion,
        }
        data.update(cambios)
        nueva = Pelicula(**data)
        actual_norm = Pelicula.normalizar_titulo(pelicula.titulo)
        nueva_norm = Pelicula.normalizar_titulo(nueva.titulo)
        if nueva_norm != actual_norm and self._existe_titulo(nueva_norm):
            raise ValueError("titulo duplicado")
        self._peliculas[indice] = nueva
        if actual_norm in self._funciones_asociadas and nueva_norm != actual_norm:
            self._funciones_asociadas.remove(actual_norm)
            self._funciones_asociadas.add(nueva_norm)
        return nueva

    def eliminar(self, titulo):
        indice, pelicula = self._buscar_por_titulo(titulo)
        normalizado = Pelicula.normalizar_titulo(pelicula.titulo)
        if normalizado in self._funciones_asociadas:
            raise ValueError("pelicula con funciones asociadas")
        self._peliculas.pop(indice)
        self._funciones_asociadas.discard(normalizado)

    def asociar_funcion(self, titulo):
        _, pelicula = self._buscar_por_titulo(titulo)
        normalizado = Pelicula.normalizar_titulo(pelicula.titulo)
        self._funciones_asociadas.add(normalizado)

    def _existe_titulo(self, normalizado):
        return any(
            Pelicula.normalizar_titulo(p.titulo) == normalizado
            for p in self._peliculas
        )

    def _buscar_por_titulo(self, titulo):
        normalizado = Pelicula.normalizar_titulo(titulo)
        for idx, pelicula in enumerate(self._peliculas):
            if Pelicula.normalizar_titulo(pelicula.titulo) == normalizado:
                return idx, pelicula
        raise ValueError("pelicula no encontrada")