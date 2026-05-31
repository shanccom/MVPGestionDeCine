from datetime import datetime


class Funcion:
    def __init__(self, pelicula, sala, fecha, hora, precio, id_funcion=None):
        self.id_funcion = self._validar_id(id_funcion, "id_funcion") if id_funcion is not None else None
        self.pelicula = self._validar_id(pelicula, "pelicula")
        self.sala = self._validar_id(sala, "sala")
        self.fecha = self._validar_fecha(fecha)
        self.hora = self._validar_hora(hora)
        self.precio = self._validar_precio(precio)

    def asignar_id(self, id_funcion):
        if self.id_funcion is not None:
            raise ValueError("id_funcion ya asignado")
        self.id_funcion = self._validar_id(id_funcion, "id_funcion")

    def obtener_id(self):
        return self.id_funcion

    def to_dict(self):
        return {
            "id_funcion": self.id_funcion,
            "pelicula": self.pelicula,
            "sala": self.sala,
            "fecha": self.fecha,
            "hora": self.hora,
            "precio": self.precio,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id_funcion=data.get("id_funcion"),
            pelicula=data["pelicula"],
            sala=data["sala"],
            fecha=data["fecha"],
            hora=data["hora"],
            precio=data["precio"],
        )

    @staticmethod
    def _validar_id(valor, nombre):
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise ValueError(f"{nombre} invalido")
        if valor <= 0:
            raise ValueError(f"{nombre} requerido")
        return valor

    @staticmethod
    def _validar_fecha(fecha):
        if not isinstance(fecha, str):
            raise ValueError("fecha invalida")
        fecha = fecha.strip()
        if not fecha:
            raise ValueError("fecha requerida")
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("fecha invalida") from exc
        return fecha

    @staticmethod
    def _validar_hora(hora):
        if not isinstance(hora, str):
            raise ValueError("hora invalida")
        hora = hora.strip()
        if not hora:
            raise ValueError("hora requerida")
        try:
            datetime.strptime(hora, "%H:%M")
        except ValueError as exc:
            raise ValueError("hora invalida") from exc
        return hora

    @staticmethod
    def _validar_precio(precio):
        if not isinstance(precio, (int, float)) or isinstance(precio, bool):
            raise ValueError("precio invalido")
        if precio <= 0:
            raise ValueError("precio fuera de rango")
        return round(float(precio), 2)
