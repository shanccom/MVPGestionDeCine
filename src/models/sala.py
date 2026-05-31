from typing import Optional

class Sala:
    """
    Modelo de dominio para Sala.
    Gestiona la validación estricta de tipos y reglas de negocio para el aforo físico.
    """
    CAPACIDAD_MIN = 1
    CAPACIDAD_MAX = 300
    NUMERO_MAX = 50

    def __init__(
        self, 
        id_sala: Optional[int] = None, 
        numero: int = 0, 
        capacidad: int = 0
    ) -> None:
        
        # 1. Validaciones de Tipo (TypeError)
        if type(numero) is not int:
            raise TypeError("El numero de sala debe ser un numero entero")
            
        if type(capacidad) is not int:
            raise TypeError("La capacidad debe ser un numero entero")
            
        if id_sala is not None and type(id_sala) is not int:
            raise TypeError("El id_sala debe ser un numero entero")

        # 2. Validaciones de Valores Límite (ValueError)
        # <-- Lógica actualizada para el número de sala
        if numero < 1 or numero > self.NUMERO_MAX:
            raise ValueError(f"El numero de sala es invalido, debe estar entre 1 y {self.NUMERO_MAX}")
            
        if capacidad < self.CAPACIDAD_MIN or capacidad > self.CAPACIDAD_MAX:
            raise ValueError(f"La capacidad de la sala debe estar en el rango entre {self.CAPACIDAD_MIN} y {self.CAPACIDAD_MAX}")
            
        if id_sala is not None and id_sala <= 0:
            raise ValueError("El id_sala debe ser mayor a cero")

        # 3. Asignación de propiedades
        self.id_sala = id_sala
        self.numero = numero
        self.capacidad = capacidad

    def to_dict(self) -> dict:
        """
        Serializa la instancia de Sala a un diccionario plano.
        Ideal para persistencia en JSON o bases de datos documentales.
        """
        return {
            "id_sala": self.id_sala,
            "numero": self.numero,
            "capacidad": self.capacidad,
        }

    @staticmethod
    def from_dict(data: dict) -> "Sala":
        """
        Fábrica para reconstruir una instancia de Sala a partir de un diccionario.
        """
        return Sala(
            id_sala=data.get("id_sala"),
            numero=data.get("numero", 0),
            capacidad=data.get("capacidad", 0),
        )