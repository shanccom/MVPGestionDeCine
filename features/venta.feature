Feature: Gestion de Ventas
  Como encargado de taquilla
  Quiero registrar la venta de entradas
  Para controlar los ingresos del cine y la ocupación de asientos

  Scenario: Registrar venta de entradas valida
    Given existen una pelicula y una funcion registradas
    When realizo la venta para la pelicula "Hola" en la funcion 1 con los asientos (1, 2, 3, 4, 5)
    Then el sistema registra la venta exitosamente
    And calcula un total de 75.0
    And el estado inicial de la venta queda como "ACTIVA"

  Scenario: Rechazar venta sin asientos seleccionados
    Given existen una pelicula y una sala registradas
    When intento vender entradas para la funcion 1 sin seleccionar asientos
    Then el sistema muestra un error de venta invalida
    And la transaccion es denegada

  Scenario: Rechazar venta por exceder el limite maximo de asientos
    Given existen una pelicula y una sala registradas
    When intento comprar entradas con 15 asientos
    Then el sistema cancela la operacion por superar el limite de 10 asientos

  Scenario: Cancelar una venta activa
    Given existe una venta registrada con estado "ACTIVA"
    When proceso la cancelacion de dicha venta usando su ID
    Then el sistema cambia el estado de la venta a "CANCELADA"

  Scenario: Evitar la duplicidad de asientos en una misma funcion
    Given que los asientos del 1 al 10 ya se encuentran ocupados en la funcion 1
    When otro usuario intenta comprar el asiento 10 para la misma funcion 1
    Then el sistema rebota la transaccion por conflicto de asientos ocupados