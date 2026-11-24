package com.dronflow.history;

import com.dronflow.monitoring.Severity;

import java.time.Instant;
import java.util.UUID;

/** Objeto de valor: una alerta alta o crítica ocurrida durante una misión. */
public record Incident(UUID alertId, String missionCode, Severity severity, Instant moment) {}
