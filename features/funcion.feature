Feature: Gestion de Funciones

  Scenario: Registrar funcion correctamente
    Given existen una pelicula y una sala registradas
    When registro una funcion con fecha "2026-06-01", hora "18:30" y precio 15.00
    Then la funcion queda registrada en el sistema

  Scenario: Registrar funcion con precio invalido
    Given existen una pelicula y una sala registradas
    When intento registrar una funcion con precio 0
    Then el sistema muestra un error de precio invalido

  Scenario: Registrar funcion sin pelicula
    Given existe una sala registrada
    When intento registrar una funcion sin pelicula
    Then el sistema muestra un error de pelicula obligatoria

  Scenario: Listar funciones registradas
    Given existen funciones registradas
    When consulto el listado de funciones
    Then el sistema muestra las funciones disponibles

  Scenario: Actualizar funcion existente
    Given existe una funcion registrada
    When modifico la hora y el precio de la funcion
    Then el sistema guarda los nuevos datos de la funcion

  Scenario: Eliminar funcion existente
    Given existe una funcion registrada
    When elimino la funcion
    Then la funcion deja de aparecer en el listado
