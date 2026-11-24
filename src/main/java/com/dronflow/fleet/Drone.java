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
        this.batteryLevelPercent = 100;
        this.location = null;
        this.state = DroneState.AVAILABLE;
    }

    /**
     * Polimorfismo: la tarea de la misión la ejecuta cada subtipo a su manera.
     * La llama MissionService al autorizar el despegue; agregar un tipo nuevo no toca a ningún llamador.
     */
    public abstract void executeTask(Mission mission);

    public void updateTelemetry(double batteryLevelPercent, Location location) {
        if (batteryLevelPercent < 0 || batteryLevelPercent > 100) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Battery level must be between 0 and 100");
        }
        this.batteryLevelPercent = batteryLevelPercent;
        this.location = location;
    }

    public boolean canExecute(double requiredPayload, int minEndurance) {
        return state == DroneState.AVAILABLE && maxPayload >= requiredPayload && enduranceMin >= minEndurance;
    }

    public void assignToMission() {
        requireState("assign to a mission", DroneState.AVAILABLE);
        state = DroneState.ON_MISSION;
    }

    public void completeMission(double batteryThreshold) {
        requireState("complete a mission", DroneState.ON_MISSION);
        state = batteryLevelPercent < batteryThreshold ? DroneState.CHARGING : DroneState.AVAILABLE;
    }

    public void finishCharging() {
        requireState("finish charging", DroneState.CHARGING);
        state = DroneState.AVAILABLE;
    }

    public void releaseReservation() {
        requireState("release", DroneState.ON_MISSION);
        state = DroneState.AVAILABLE;
    }

    public void markOutOfService() {
        requireState("report a fault", DroneState.AVAILABLE);
        state = DroneState.OUT_OF_SERVICE;
    }

    public void sendToMaintenance() {
        requireState("send to maintenance", DroneState.AVAILABLE, DroneState.ON_MISSION, DroneState.CHARGING);
        state = DroneState.IN_MAINTENANCE;
    }

    public void sendToRepair() {
        requireState("send to repair", DroneState.IN_MAINTENANCE);
        state = DroneState.OUT_OF_SERVICE;
    }

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
