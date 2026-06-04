from typing import List, Optional
from models.sala import Sala
from storage.salas.sala_repository import SalaRepository

class SalaService:

    def __init__(self, repository: SalaRepository) -> None:
        self.repository = repository

    def registrar_sala(self, numero: int, capacidad: int) -> Sala:
        nueva_sala = Sala(numero=numero, capacidad=capacidad)
        
        self.repository.guardar(nueva_sala)
        
        return nueva_sala

    def listar_salas(self) -> List[Sala]:
        return self.repository.listar()

    def buscar_sala_por_id(self, id_sala: int) -> Optional[Sala]:
        if type(id_sala) is not int:
            raise TypeError("El id_sala debe ser un numero entero")

        sala = self.repository.buscar_por_id(id_sala)
        if not sala:
            raise ValueError(f"No se encontro ninguna sala con el ID {id_sala}.")
            
        return sala

    def actualizar_sala(self, id_sala: int, numero: int, capacidad: int) -> Sala:
        self.buscar_sala_por_id(id_sala)

        sala_actualizada = Sala(id_sala=id_sala, numero=numero, capacidad=capacidad)

        self.repository.guardar(sala_actualizada)

        return sala_actualizada

    def eliminar_sala(self, id_sala: int) -> None:
        if type(id_sala) is not int:
            raise TypeError("El id_sala debe ser un numero entero")
            
        self.repository.eliminar(id_sala)