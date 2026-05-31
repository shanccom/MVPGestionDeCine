Feature: Gestion de salas
Característica: Gestión del Módulo de Salas
  Como administrador del cine
  Quiero gestionar la información de las salas físicas
  Para controlar el aforo y habilitar la programación de funciones

  Escenario: Creación exitosa de una sala
    Dado que ingreso a la opción de registrar nueva sala
    Cuando ingreso el número "5"
    Y la capacidad "150"
    Y guardo los cambios
    Entonces el sistema registra la sala exitosamente
    Y se le asigna un "id_sala" autogenerado internamente

  Escenario: Error por duplicado de número de sala
    Dado que ya existe una sala registrada con el número "3"
    Cuando intento registrar una nueva sala con el número "3"
    Y una capacidad de "120"
    Y guardo los cambios
    Entonces el sistema rechaza el registro
    Y muestra un mensaje de error indicando que el número de sala ya está en uso

  Escenario: Error por capacidad fuera de rango
    Dado que ingreso a la opción de registrar nueva sala
    Cuando ingreso el número "4"
    Y la capacidad "350"
    Entonces el sistema lanza una excepción de valor
    Y el registro es denegado por exceder la capacidad máxima de 300 asientos

  Escenario: Bloqueo de eliminación por dependencias
    Dado que la sala con número "1" tiene funciones de cine programadas para el fin de semana
    Cuando intento eliminar la sala número "1"
    Entonces el sistema bloquea la acción
    Y advierte que no se puede eliminar una sala con funciones asociadas