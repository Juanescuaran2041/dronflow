package com.dronflow.maintenance;

import com.dronflow.configuration.MaintenanceThresholds;
import com.dronflow.configuration.SystemConfigurationService;
import com.dronflow.fleet.DroneService;
import com.dronflow.history.HistoryUpdated;
import com.dronflow.monitoring.Alert;
import com.dronflow.monitoring.AlertService;
import com.dronflow.monitoring.AlertType;
import org.springframework.context.event.EventListener;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MaintenanceRecommendationService {
    private final MaintenanceRecommendationRepository recommendationRepository;
    private final SystemConfigurationService configuration;
    private final DroneService droneService;
    private final AlertService alertService;

    public MaintenanceRecommendationService(MaintenanceRecommendationRepository recommendationRepository,
                                            SystemConfigurationService configuration, DroneService droneService,
                                            AlertService alertService) {
        this.recommendationRepository = recommendationRepository;
        this.configuration = configuration;
        this.droneService = droneService;
        this.alertService = alertService;
    }

    /**
     * Al actualizarse el historial, si el dron supera el umbral se genera la recomendación,
     * el dron pasa a "en mantenimiento" y el administrador ve una alerta en pantalla.
     */
    @EventListener
    public void onHistoryUpdated(HistoryUpdated event) {
        MaintenanceThresholds thresholds = configuration.getMaintenanceThresholds();
        if (!thresholds.exceededBy(event.flightHours(), event.completedMissions())) {
            return;
        }
        String reason = String.format("%.1f flight hours and %d missions (thresholds: %.0f h or %d missions)",
                event.flightHours(), event.completedMissions(), thresholds.maxHours(), thresholds.maxMissions());
        recommendationRepository.save(new MaintenanceRecommendation(event.droneCode(), reason));
        droneService.sendToMaintenance(event.droneCode());
        alertService.raise(new Alert(AlertType.MAINTENANCE, event.droneCode(), null,
                "Preventive maintenance recommended: " + reason));
    }

    public List<MaintenanceRecommendation> list() {
        return recommendationRepository.findAllByOrderByGeneratedAtDesc();
    }
}
