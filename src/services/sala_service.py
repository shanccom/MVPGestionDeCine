from typing import List, Optional
from models.sala import Sala
from storage.salas.sala_repository import SalaRepository

class SalaService:
    """
    Capa de servicio para el módulo de Salas.
    Orquesta las reglas de negocio y sirve como puente entre la interfaz de usuario
    y la capa de persistencia (repositorio).
    """

    def __init__(self, repository: SalaRepository) -> None:
        self.repository = repository

    def registrar_sala(self, numero: int, capacidad: int) -> Sala:
        """
        Crea una nueva sala, ejecutando las validaciones del modelo, 
        y la persiste delegando al repositorio.
        """
        nueva_sala = Sala(numero=numero, capacidad=capacidad)
        
        self.repository.guardar(nueva_sala)
        
        return nueva_sala

    def listar_salas(self) -> List[Sala]:
        """
        Recupera la lista de todas las salas ordenadas por número.
        """
        return self.repository.listar()

    def buscar_sala_por_id(self, id_sala: int) -> Optional[Sala]:
        """
        Busca una sala específica por su identificador único.
        Lanza ValueError si la sala no es encontrada.
        """
        if type(id_sala) is not int:
            raise TypeError("El id_sala debe ser un numero entero")

        sala = self.repository.buscar_por_id(id_sala)
        if not sala:
            raise ValueError(f"No se encontro ninguna sala con el ID {id_sala}.")
            
        return sala

    def actualizar_sala(self, id_sala: int, numero: int, capacidad: int) -> Sala:
        """
        Actualiza los datos de una sala existente, reevaluando las validaciones de límites.
        """
        # 1. Verificamos que la sala existe (este método lanza ValueError si no es así)
        self.buscar_sala_por_id(id_sala)

        # 2. Instanciamos un nuevo objeto Sala para forzar que los nuevos parámetros 
        # pasen por las reglas de negocio y blindaje sintáctico/semántico.
        sala_actualizada = Sala(id_sala=id_sala, numero=numero, capacidad=capacidad)

        # 3. Delegamos el guardado al repositorio (actualizará el registro existente 
        # y validará que el nuevo número no choque con el de otra sala).
        self.repository.guardar(sala_actualizada)

        return sala_actualizada

    def eliminar_sala(self, id_sala: int) -> None:
        """
        Solicita la eliminación de una sala del sistema.
        """
        if type(id_sala) is not int:
            raise TypeError("El id_sala debe ser un numero entero")
            
        # El repositorio se encargará de verificar la regla de negocio de "no eliminar 
        # si tiene funciones asociadas" y levantará un ValueError si la validación falla.
        self.repository.eliminar(id_sala)