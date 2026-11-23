package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;
import org.springframework.stereotype.Component;

@Component
public class MonitoringDroneFactory implements DroneFactory {

    @Override
    public String type() {
        return "monitoring";
    }

    @Override
    public Drone create(RegisterDroneRequest data) {
        return new MonitoringDrone(data);
    }
}
