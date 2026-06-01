class Pelicula:
    GENEROS = {
        "Accion",
        "Comedia",
        "Drama",
        "Terror",
        "Animacion",
        "Ciencia Ficcion",
        "Documental",
        "Romance",
        "Aventura",
        "Fantasia",
    }
    TITULO_MIN = 1
    TITULO_MAX = 100
    DURACION_MIN = 60
    DURACION_MAX = 240

    def __init__(self, titulo, genero, duracion, id_pelicula=None):
        self.id_pelicula = (
            self._validar_id(id_pelicula) if id_pelicula is not None else None
        )
        self.titulo = self._validar_titulo(titulo)
        self.genero = self._validar_genero(genero)
        self.duracion = self._validar_duracion(duracion)

    def asignar_id(self, id_pelicula):
        if self.id_pelicula is not None:
            raise ValueError("id_pelicula ya asignado")
        self.id_pelicula = self._validar_id(id_pelicula)

    def obtener_id(self):
        return self.id_pelicula

    @classmethod
    def normalizar_titulo(cls, titulo):
        limpio = cls._limpiar_titulo(titulo)
        return limpio.lower()

    @classmethod
    def _limpiar_titulo(cls, titulo):
        if not isinstance(titulo, str):
            raise ValueError("titulo invalido")
        return titulo.strip()

    @classmethod
    def _validar_titulo(cls, titulo):
        limpio = cls._limpiar_titulo(titulo)
        if not limpio:
            raise ValueError("titulo requerido")
        if len(limpio) < cls.TITULO_MIN or len(limpio) > cls.TITULO_MAX:
            raise ValueError("titulo fuera de rango")
        return limpio

    @classmethod
    def _validar_genero(cls, genero):
        if not isinstance(genero, str):
            raise ValueError("genero invalido")
        genero = genero.strip()
        if not genero:
            raise ValueError("genero requerido")
        if genero not in cls.GENEROS:
            raise ValueError("genero fuera de catalogo")
        return genero

    @classmethod
    def _validar_duracion(cls, duracion):
        if not isinstance(duracion, int) or isinstance(duracion, bool):
            raise ValueError("duracion invalida")
        if duracion < cls.DURACION_MIN or duracion > cls.DURACION_MAX:
            raise ValueError("duracion fuera de rango")
        return duracion

    @staticmethod
    def _validar_id(id_pelicula):
        if not isinstance(id_pelicula, int) or isinstance(id_pelicula, bool):
            raise ValueError("id_pelicula invalido")
        if id_pelicula <= 0:
            raise ValueError("id_pelicula invalido")
        return id_pelicula