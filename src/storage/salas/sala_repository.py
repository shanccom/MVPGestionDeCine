import json
import os
from typing import List, Optional
from models.sala import Sala

class SalaRepository:
    def __init__(self, archivo_json: str = "data/salas.json") -> None:
        self.archivo_json = archivo_json
        self._asegurar_archivo()

    def _asegurar_archivo(self) -> None:
        """Crea el directorio y el archivo JSON inicial si no existen."""
        directorio = os.path.dirname(self.archivo_json)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        if not os.path.exists(self.archivo_json):
            self._guardar_datos([])

    def _cargar_datos(self) -> List[dict]:
        """Lee y retorna los datos puros del archivo JSON."""
        try:
            with open(self.archivo_json, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _guardar_datos(self, datos: List[dict]) -> None:
        """Escribe la estructura de datos en el archivo JSON."""
        with open(self.archivo_json, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4)

    def listar(self) -> List[Sala]:
        """
        Carga el JSON, mapea a instancias de Sala y devuelve la lista 
        ordenada ascendentemente por el campo 'numero'.
        """
        datos = self._cargar_datos()
        salas = [Sala.from_dict(d) for d in datos]
        salas.sort(key=lambda s: s.numero)
        return salas

    def buscar_por_id(self, id_sala: int) -> Optional[Sala]:
        """Retorna la instancia de sala correspondiente o None si no existe."""
        for sala in self.listar():
            if sala.id_sala == id_sala:
                return sala
        return None

    def buscar_por_numero(self, numero: int) -> Optional[Sala]:
        """
        Retorna la sala por su número físico/comercial. 
        Útil para validaciones y tests Gherkin.
        """
        for sala in self.listar():
            if sala.numero == numero:
                return sala
        return None

    def guardar(self, sala: Sala) -> None:
        """
        Inserta una nueva sala con ID autoincremental o actualiza una existente.
        Valida que el número de sala no esté duplicado.
        """
        salas_existentes = self.listar()

        # Validación de duplicidad (excluyendo a la sala misma si se está actualizando)
        for s in salas_existentes:
            if s.numero == sala.numero and s.id_sala != sala.id_sala:
                raise ValueError("El número de sala ya está en uso")

        if sala.id_sala is None:
            # Lógica autoincremental
            nuevo_id = 1
            if salas_existentes:
                nuevo_id = max(s.id_sala for s in salas_existentes) + 1
            sala.id_sala = nuevo_id
            salas_existentes.append(sala)
        else:
            # Lógica de actualización
            indice = next((i for i, s in enumerate(salas_existentes) if s.id_sala == sala.id_sala), None)
            if indice is not None:
                salas_existentes[indice] = sala
            else:
                raise ValueError("No se puede actualizar: el id_sala no existe en los registros")

        # Serialización y guardado
        datos_serializados = [s.to_dict() for s in salas_existentes]
        self._guardar_datos(datos_serializados)

    def tiene_funciones_asociadas(self, id_sala: int) -> bool:
        """
        Simulador de regla de negocio. Por defecto retorna False.
        En producción consultaría el módulo de funciones.
        """
        return False

    def eliminar(self, id_sala: int) -> None:
        """
        Elimina la sala del JSON si no rompe la integridad referencial.
        """
        if self.tiene_funciones_asociadas(id_sala):
            raise ValueError("No se puede eliminar una sala con funciones asociadas")

        salas = self.listar()
        salas_filtradas = [s for s in salas if s.id_sala != id_sala]

        if len(salas) == len(salas_filtradas):
            raise ValueError("No se pudo eliminar: el id_sala no existe")

        datos_serializados = [s.to_dict() for s in salas_filtradas]
        self._guardar_datos(datos_serializados)