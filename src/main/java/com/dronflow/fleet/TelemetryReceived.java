package com.dronflow.fleet;

/**
 * Observer: lo escucha AlertService para aplicar sus reglas de alerta.
 * Lleva el dron ya actualizado y guardado para que quien lo escuche no tenga que volver a leerlo.
 */
public record TelemetryReceived(Drone drone) {}
