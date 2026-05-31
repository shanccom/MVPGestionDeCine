Feature: Gestion de peliculas
  Como responsable de catalogo
  Quiero gestionar peliculas
  Para programar funciones en el cine

  Background:
    Given el catalogo de generos y clasificaciones esta disponible

  Scenario: Registrar pelicula valida
    Given estoy en el formulario de pelicula
    When ingreso titulo "Matrix", genero "Ciencia Ficcion", duracion 136, clasificacion "14+"
    And guardo la pelicula
    Then el sistema registra la pelicula
    And la pelicula aparece en el listado

  Scenario: Rechazar duracion fuera de rango
    Given estoy en el formulario de pelicula
    When ingreso titulo "Corta", genero "Comedia", duracion 0, clasificacion "APT"
    And guardo la pelicula
    Then el sistema muestra el error "duracion fuera de rango"
    And no se registra la pelicula

  Scenario: Evitar duplicidad de titulo
    Given existe la pelicula "Matrix"
    When registro una pelicula con titulo " matrix ", genero "Ciencia Ficcion", duracion 136, clasificacion "14+"
    Then el sistema muestra el error "titulo duplicado"
    And no se registra la pelicula

  Scenario: Editar pelicula
    Given existe la pelicula "Matrix"
    When actualizo la duracion a 140
    Then el sistema guarda los cambios

  Scenario: Eliminar pelicula sin funciones asociadas
    Given existe la pelicula "Matrix" sin funciones asociadas
    When elimino la pelicula
    Then el sistema elimina la pelicula

  Scenario: Bloquear eliminacion con funciones asociadas
    Given existe la pelicula "Matrix" con funciones asociadas
    When intento eliminar la pelicula
    Then el sistema muestra el error "pelicula con funciones asociadas"
    And no se elimina la pelicula