from models.funcion import Funcion
from storage.funciones.funcion_repository import FuncionRepository


class FuncionService:
    def __init__(self, ruta=None, repository=None):
        self._repo = repository or FuncionRepository(ruta)

    def crear_funcion(self, pelicula, sala, fecha, hora, precio):
        funcion = Funcion(
            pelicula=pelicula,
            sala=sala,
            fecha=fecha,
            hora=hora,
            precio=precio,
        )
        return self._repo.guardar(funcion)

    def obtener_todas(self):
        return self._repo.listar()

    def buscar_por_id(self, id_funcion):
        return self._repo.buscar_por_id(id_funcion)

    def actualizar_funcion(self, id_funcion, pelicula, sala, fecha, hora, precio):
        return self._repo.actualizar(
            id_funcion,
            pelicula=pelicula,
            sala=sala,
            fecha=fecha,
            hora=hora,
            precio=precio,
        )

    def eliminar_funcion(self, id_funcion):
        return self._repo.eliminar(id_funcion)

    def registrar(self, pelicula, sala, fecha, hora, precio):
        return self.crear_funcion(pelicula, sala, fecha, hora, precio)

    def listar(self):
        return self.obtener_todas()

    def actualizar(self, id_funcion, **cambios):
        actual = self.buscar_por_id(id_funcion)
        data = actual.to_dict()
        data.update(cambios)
        data.pop("id_funcion", None)
        return self.actualizar_funcion(id_funcion, **data)

    def eliminar(self, id_funcion):
        return self.eliminar_funcion(id_funcion)
