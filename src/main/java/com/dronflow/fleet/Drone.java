package com.dronflow.fleet;

import com.dronflow.mission.Mission;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.http.HttpStatus;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;

// Los tres subtipos se guardan en la misma colección; Spring Data agrega "_class" para saber cuál crear al leer.
@Document("drones")
public abstract class Drone {

    @Id
    private String code;
    private String type;
    private int batteryCapacity;
    private double batteryLevelPercent;
    private int enduranceMin;
    private double maxPayload;
    private List<String> equipment;
    private Location location;
    private DroneState state;

    protected Drone() {}

    protected Drone(String code, String type, int batteryCapacity, int enduranceMin,
                    double maxPayload, List<String> equipment) {
        this.code = code;
        this.type = type;
        this.batteryCapacity = batteryCapacity;
        this.enduranceMin = enduranceMin;
        this.maxPayload = maxPayload;
        this.equipment = equipment;
        this.batteryLevelPercent = 100; // pendiente de confirmar por el autor: HU-01 no da el nivel inicial
        this.location = null;           // pendiente de confirmar: se conoce con la primera telemetría
        this.state = DroneState.AVAILABLE; // HU-02: un dron recién registrado queda disponible
    }

    /**
     * RF-02: la tarea de la misión la ejecuta cada subtipo a su manera (entrega, inspección, monitoreo).
     * La llama MissionService al autorizar el despegue; agregar un tipo nuevo no toca a ningún llamador.
     */
    public abstract void executeTask(Mission mission);

    // HU-09/HU-10: cada lectura del dron en vuelo actualiza su batería y su posición
    public void updateTelemetry(double batteryLevelPercent, Location location) {
        if (batteryLevelPercent < 0 || batteryLevelPercent > 100) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Battery level must be between 0 and 100");
        }
        this.batteryLevelPercent = batteryLevelPercent;
        this.location = location;
    }

    // HU-05: el dron sirve si soporta la carga y la autonomía que pide la misión
    public boolean canExecute(double requiredPayload, int minEndurance) {
        return state == DroneState.AVAILABLE && maxPayload >= requiredPayload && enduranceMin >= minEndurance;
    }

    // HU-05: al asignarlo queda reservado ("en misión")
    public void assignToMission() {
        requireState("assign to a mission", DroneState.AVAILABLE);
        state = DroneState.ON_MISSION;
    }

    // HU-06: se libera si no se logra validar la ruta
    public void releaseReservation() {
        requireState("release", DroneState.ON_MISSION);
        state = DroneState.AVAILABLE;
    }

    // HU-02: un operador reporta una avería
    public void markOutOfService() {
        requireState("report a fault", DroneState.AVAILABLE);
        state = DroneState.OUT_OF_SERVICE;
    }

    // HU-14: la recomendación de mantenimiento lo saca de servicio
    public void sendToMaintenance() {
        requireState("send to maintenance", DroneState.AVAILABLE, DroneState.ON_MISSION, DroneState.CHARGING);
        state = DroneState.IN_MAINTENANCE;
    }

    // HU-15: el mantenimiento concluye que necesita reparación
    public void sendToRepair() {
        requireState("send to repair", DroneState.IN_MAINTENANCE);
        state = DroneState.OUT_OF_SERVICE;
    }

    // HU-03: baja permanente, solo sin misión activa
    public void decommission() {
        if (state == DroneState.ON_MISSION) {
            throw new ResponseStatusException(HttpStatus.CONFLICT,
                    "The drone has an active mission: finish or abort it first");
        }
        if (state == DroneState.DECOMMISSIONED) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "The drone is already decommissioned");
        }
        state = DroneState.DECOMMISSIONED;
    }

    // HU-03: vuelve al servicio desde fuera de servicio o en mantenimiento
    public void reactivate() {
        requireState("reactivate", DroneState.OUT_OF_SERVICE, DroneState.IN_MAINTENANCE);
        state = DroneState.AVAILABLE;
    }

    private void requireState(String action, DroneState... allowed) {
        for (DroneState s : allowed) {
            if (state == s) return;
        }
        throw new ResponseStatusException(HttpStatus.CONFLICT,
                "Cannot " + action + ": the drone is " + state);
    }

    public String getCode() { return code; }
    public String getType() { return type; }
    public int getBatteryCapacity() { return batteryCapacity; }
    public double getBatteryLevelPercent() { return batteryLevelPercent; }
    public int getEnduranceMin() { return enduranceMin; }
    public double getMaxPayload() { return maxPayload; }
    public List<String> getEquipment() { return equipment; }
    public Location getLocation() { return location; }
    public DroneState getState() { return state; }
}
