package com.dronflow.history;

import com.dronflow.fleet.DroneService;
import com.dronflow.mission.MissionCompleted;
import com.dronflow.monitoring.AlertService;
import org.springframework.context.ApplicationEventPublisher;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Service;

@Service
public class FlightHistoryService {
    private final FlightHistoryRepository historyRepository;
    private final AlertService alertService;
    private final DroneService droneService;
    private final ApplicationEventPublisher events;

    public FlightHistoryService(FlightHistoryRepository historyRepository, AlertService alertService,
                                DroneService droneService, ApplicationEventPublisher events) {
        this.historyRepository = historyRepository;
        this.alertService = alertService;
        this.droneService = droneService;
        this.events = events;
    }

    public FlightHistory getHistory(String droneCode) {
        droneService.findByCode(droneCode); // 404 si el dron no existe
        return historyRepository.findById(droneCode).orElseGet(() -> new FlightHistory(droneCode));
    }

    @EventListener
    public void onMissionCompleted(MissionCompleted event) {
        FlightHistory history = historyRepository.findById(event.droneCode())
                .orElseGet(() -> new FlightHistory(event.droneCode()));
        history.registerCompletedMission(event.flightDuration());
        alertService.alertsOfMission(event.missionCode()).forEach(history::registerIncident);
        historyRepository.save(history);
        events.publishEvent(new HistoryUpdated(history.getDroneCode(), history.getFlightHours(), history.getCompletedMissions()));
    }

    public void resetCounters(String droneCode) {
        FlightHistory history = getHistory(droneCode);
        history.resetCounters();
        historyRepository.save(history);
    }
}
