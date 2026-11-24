package com.dronflow.fleet;

/**
 * Evento: llegó una lectura del dron (HU-09, HU-10). Lo escucha AlertService para aplicar sus reglas.
 * Lleva el dron ya actualizado y guardado para que quien lo escuche no tenga que volver a leerlo.
 */
public record TelemetryReceived(Drone drone) {}
