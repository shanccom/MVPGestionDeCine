from models.pelicula import Pelicula

class PeliculaService:
    def __init__(self, repository=None):
        self._repo = repository
        self._peliculas = []
        self._next_id = 1
        self._funciones_asociadas = set()

    def registrar(self, titulo, genero, duracion):
        if self._repo is not None:
            pelicula = Pelicula(
                titulo=titulo,
                genero=genero,
                duracion=duracion,
            )
            return self._repo.guardar(pelicula)
        pelicula = Pelicula(
            titulo=titulo,
            genero=genero,
            duracion=duracion,
            id_pelicula=self._next_id,
        )
        self._next_id += 1
        self._peliculas.append(pelicula)
        return pelicula

    def listar(self):
        if self._repo is not None:
            return self._repo.listar()
        return list(self._peliculas)

    def actualizar(self, id_pelicula, **cambios):
        cambios.pop("id_pelicula", None)
        if self._repo is not None:
            return self._repo.actualizar(id_pelicula, **cambios)
        indice, pelicula = self._buscar_por_id(id_pelicula)
        data = {
            "id_pelicula": pelicula.id_pelicula,
            "titulo": pelicula.titulo,
            "genero": pelicula.genero,
            "duracion": pelicula.duracion,
        }
        data.update(cambios)
        nueva = Pelicula(**data)
        self._peliculas[indice] = nueva
        return nueva

    def eliminar(self, id_pelicula):
        indice, pelicula = self._buscar_por_id(id_pelicula)
        if pelicula.id_pelicula in self._funciones_asociadas:
            raise ValueError("pelicula con funciones asociadas")
        if self._repo is not None:
            self._repo.eliminar(id_pelicula)
        else:
            self._peliculas.pop(indice)
        self._funciones_asociadas.discard(pelicula.id_pelicula)

    def asociar_funcion(self, id_pelicula):
        _, pelicula = self._buscar_por_id(id_pelicula)
        self._funciones_asociadas.add(pelicula.id_pelicula)

    def _buscar_por_id(self, id_pelicula):
        if self._repo is not None:
            pelicula = self._repo.buscar_por_id(id_pelicula)
            return None, pelicula
        for idx, pelicula in enumerate(self._peliculas):
            if pelicula.id_pelicula == id_pelicula:
                return idx, pelicula
        raise ValueError("pelicula no encontrada")