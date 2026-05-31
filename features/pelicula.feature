Feature: Gestion de peliculas
  Como responsable de catalogo
  Quiero gestionar peliculas
  Para programar funciones en el cine

  Background:
    Given el catalogo de generos esta disponible

  Scenario: Registrar pelicula valida
    Given estoy en el formulario de pelicula
    When ingreso titulo "Matrix", genero "Ciencia Ficcion", duracion 136
    And guardo la pelicula
    Then el sistema registra la pelicula
    And el sistema asigna id_pelicula
    And la pelicula aparece en el listado

  Scenario: Rechazar duracion fuera de rango
    Given estoy en el formulario de pelicula
    When ingreso titulo "Corta", genero "Comedia", duracion 59
    And guardo la pelicula
    Then el sistema muestra el error "duracion fuera de rango"
    And no se registra la pelicula

  Scenario: Editar pelicula
    Given existe la pelicula con id 1
    When actualizo la duracion a 140 para la pelicula 1
    Then el sistema guarda los cambios

  Scenario: Eliminar pelicula sin funciones asociadas
    Given existe la pelicula con id 1 sin funciones asociadas
    When elimino la pelicula 1
    Then el sistema elimina la pelicula

  Scenario: Bloquear eliminacion con funciones asociadas
    Given existe la pelicula con id 1 con funciones asociadas
    When intento eliminar la pelicula 1
    Then el sistema muestra el error "pelicula con funciones asociadas"
    And no se elimina la pelicula