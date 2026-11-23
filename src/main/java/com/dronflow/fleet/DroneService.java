package com.dronflow.fleet;

import com.dronflow.fleet.dto.RegisterDroneRequest;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.Map;
import java.util.function.Function;
import java.util.stream.Collectors;

@Service
public class DroneService {
    private final DroneRepository droneRepository;
    private final Map<String, DroneFactory> factories;
    private final ApplicationEventPublisher events;

    // Spring inyecta todas las fábricas registradas (@Component); se indexan por su tipo.
    public DroneService(DroneRepository droneRepository, List<DroneFactory> factories, ApplicationEventPublisher events) {
        this.droneRepository = droneRepository;
        this.events = events;
        this.factories = factories.stream().collect(Collectors.toMap(DroneFactory::type, Function.identity()));
    }

    public Drone register(RegisterDroneRequest data) {
        DroneFactory factory = factories.get(data.type());
        if (factory == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST,
                    "Unsupported drone type. Supported types: " + factories.keySet());
        }
        if (droneRepository.existsById(data.code())) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Drone code already in use");
        }
        return droneRepository.save(factory.create(data));
    }

    // HU-03: un dron dado de baja deja de aparecer entre los drones de la flota
    public List<Drone> listAll() {
        return droneRepository.findByStateNot(DroneState.DECOMMISSIONED);
    }

    public Drone findByCode(String code) {
        return droneRepository.findById(code)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Drone not found"));
    }

    public Drone reportFault(String code) {
        Drone drone = findByCode(code);
        drone.markOutOfService();
        return droneRepository.save(drone);
    }

    public Drone decommission(String code) {
        Drone drone = findByCode(code);
        drone.decommission();
        return droneRepository.save(drone);
    }

    public Drone reactivate(String code) {
        Drone drone = findByCode(code);
        drone.reactivate();
        Drone saved = droneRepository.save(drone);
        events.publishEvent(new DroneAvailable(code)); // HU-05: puede tomar una misión pendiente
        return saved;
    }

    public List<Drone> findAvailable() {
        return droneRepository.findByState(DroneState.AVAILABLE);
    }

    public Drone reserve(String code) {
        Drone drone = findByCode(code);
        drone.assignToMission();
        return droneRepository.save(drone);
    }

    // No publica DroneAvailable: la misión que lo liberó no debe volver a tomarlo de inmediato (HU-06)
    public Drone release(String code) {
        Drone drone = findByCode(code);
        drone.releaseReservation();
        return droneRepository.save(drone);
    }
}
