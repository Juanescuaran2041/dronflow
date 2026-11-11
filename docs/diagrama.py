import sys
from componentes_lib import Diagrama

d = Diagrama("Dronflow - Diagrama de componentes", ancho=2800, alto=1640)

# ---------------- componentes ----------------
d.componente( 370,   70, "Gestion de\nUsuarios",             w=250, h=150)
d.componente( 370,  280, "Autenticacion",                    w=250, h=110)
d.componente( 370,  450, "Gestion de\nMisiones",             w=250, h=400)
d.componente( 370,  910, "Panel de Control",                 w=250, h=110)
d.componente( 900,  450, "Asignacion de\nDrones",            w=250, h=110)
d.componente( 900,  660, "Validacion de\nRutas",             w=250, h=110)
d.componente( 900,  880, "Proveedor de Zonas\nRestringidas", w=280, h=110, estereotipo="«external»")
d.componente(1280,  120, "Notificacion en\nTiempo Real",     w=280, h=110)
d.componente(1280,  560, "Gestion de Flota",                 w=300, h=360)
d.componente(1280, 1120, "Configuracion del\nSistema",       w=300, h=150)
d.componente(1980,  280, "Gestion Monitoreo\ny Alertas",     w=280, h=150)
d.componente(1980,  560, "Gestion de\nMantenimientos",       w=280, h=250)
d.componente(1980,  940, "Gestion de Vuelos",                w=280, h=150)

# ===================================================================
# A. Interfaces ofrecidas sin conector: las invoca el actor, o su
#    disparador queda fuera de alcance. Bola sin enchufe.
# ===================================================================

for y, nombre in [(105, "IRegisterOperator"), (145, "IEditUser"), (185, "IDeleteUser"),
                  (335, "ILogin"),
                  (485, "ICreateMission"), (520, "IAuthorizeTakeoff"), (555, "ITakeOff"),
                  (590, "IReachCruise"), (625, "IStartReturn"), (660, "IFinishMission"),
                  (695, "IPauseMission"), (730, "IResumeMission"), (765, "IRedirectMission"),
                  (800, "IAbortMission"),
                  (945, "IGetFleetSummary"), (985, "IQueryMissions")]:
    d.interfaz((320, y + 4, nombre, "end"), proveedor=[(370, y), (340, y)])

# Configuracion del Sistema: las tres de actualizacion, por el borde inferior
for x, yb, nombre in [(1320, 1340, "IUpdateAssignmentRule"),
                      (1400, 1390, "IUpdateAlertThresholds"),
                      (1480, 1440, "IUpdateMaintenanceThresholds")]:
    d.interfaz((x, yb + 22, nombre, "middle"), proveedor=[(x, 1270), (x, yb)])

# Gestion de Flota: borde inferior
d.interfaz((1320, 1022, "IRegisterDrone", "middle"),  proveedor=[(1320, 920), (1320, 1000)])
d.interfaz((1480, 1022, "IFinishCharging", "middle"), proveedor=[(1480, 920), (1480, 1000)])

# Monitoreo, Mantenimientos y Vuelos: borde derecho
d.interfaz((2375, 334, "IEvaluateDrone", "start"),           proveedor=[(2260, 330), (2360, 330)])
d.interfaz((2375, 689, "IRecordMaintenanceResult", "start"), proveedor=[(2260, 685), (2360, 685)])
d.interfaz((2375, 1019, "IGetFlightHistory", "start"),       proveedor=[(2260, 1015), (2360, 1015)])

# ===================================================================
# B. Conectores de ensamble (28)
# ===================================================================

# 1: Usuarios -> Autenticacion
d.interfaz((505, 254, "IHashPassword", "start"),
           proveedor=[(490, 280), (490, 250)],
           consumidores=[[(490, 220), (490, 250)]])

# 16: Notificacion -> Autenticacion
d.interfaz((700, 323, "IAuthorize", "middle"),
           proveedor=[(620, 335), (700, 335)],
           consumidores=[[(1280, 175), (1230, 175), (1230, 335), (700, 335)]],
           saltos=[(1230, 205), (1230, 250)])

# 17: Panel de Control -> Notificacion (rodea por el perimetro)
d.interfaz((1150, 193, "ISubscribeToAlerts", "end"),
           proveedor=[(1280, 205), (1210, 205)],
           consumidores=[[(520, 1020), (520, 1540), (2760, 1540), (2760, 60), (1210, 60), (1210, 205)]])

# 19: Panel de Control -> Misiones
d.interfaz((505, 884, "IFindMissions", "start"),
           proveedor=[(490, 850), (490, 880)],
           consumidores=[[(490, 910), (490, 880)]])

# 18: Panel de Control -> Flota
d.interfaz((1180, 862, "IListDrones", "end"),
           proveedor=[(1280, 880), (1215, 880)],
           consumidores=[[(580, 1020), (580, 1070), (1215, 1070), (1215, 880)]])

# 2 y 3: Misiones -> Asignacion de Drones
d.interfaz((760, 468, "IAssignDrone", "middle"),
           proveedor=[(900, 480), (760, 480)],
           consumidores=[[(620, 480), (760, 480)]])
d.interfaz((760, 518, "IChooseMission", "middle"),
           proveedor=[(900, 530), (760, 530)],
           consumidores=[[(620, 530), (760, 530)]])

# 4, 5, 6: Misiones -> Flota
d.interfaz((1000, 578, "IReserveDrone", "middle"),
           proveedor=[(1280, 590), (1000, 590)],
           consumidores=[[(620, 590), (1000, 590)]])
d.interfaz((800, 618, "IReleaseDrone", "middle"),
           proveedor=[(1280, 630), (800, 630)],
           consumidores=[[(620, 630), (800, 630)]])
d.interfaz((800, 808, "ICompleteMission", "middle"),
           proveedor=[(1280, 820), (800, 820)],
           consumidores=[[(620, 820), (800, 820)]])

# 7: Misiones -> Validacion de Rutas
d.interfaz((760, 703, "IValidateRoute", "middle"),
           proveedor=[(900, 715), (760, 715)],
           consumidores=[[(620, 715), (760, 715)]])

# 8: Asignacion de Drones -> Flota
d.interfaz((1340, 468, "IFindAvailableDrones", "middle"),
           proveedor=[(1340, 560), (1340, 520)],
           consumidores=[[(1150, 480), (1340, 480), (1340, 520)]])

# 9: Asignacion de Drones -> Configuracion
d.interfaz((1225, 1215, "IGetAssignmentRule", "end"),
           proveedor=[(1280, 1190), (1255, 1190)],
           consumidores=[[(1150, 540), (1255, 540), (1255, 1190)]],
           saltos=[(1255, 590), (1255, 630), (1255, 820), (1255, 880)])

# 10 y 11 (compartida): Flota y Monitoreo -> Configuracion
d.interfaz((1415, 1070, "IGetAlertThresholds", "start"),
           proveedor=[(1400, 1120), (1400, 1040)],
           consumidores=[[(1400, 920), (1400, 1040)],
                         [(1980, 400), (1870, 400), (1870, 1040), (1400, 1040)]],
           saltos=[(1870, 430), (1870, 590), (1870, 640), (1870, 690),
                   (1870, 740), (1870, 790), (1870, 900)])

# 12: Monitoreo -> Flota
d.interfaz((1750, 578, "IFindDrone", "middle"),
           proveedor=[(1580, 590), (1750, 590)],
           consumidores=[[(1980, 360), (1920, 360), (1920, 590), (1750, 590)]],
           saltos=[(1920, 400), (1920, 430)])

# 13: Monitoreo -> Misiones
d.interfaz((780, 758, "IFindMission", "middle"),
           proveedor=[(620, 770), (860, 770)],
           consumidores=[[(2040, 280), (2040, 250), (860, 250), (860, 770)]],
           saltos=[(860, 335), (860, 440), (860, 480), (860, 530),
                   (860, 590), (860, 630), (860, 715)])

# 14: Monitoreo -> Validacion de Rutas
d.interfaz((1197, 745, "ICheckPosition", "middle"),
           proveedor=[(1150, 715), (1200, 715)],
           consumidores=[[(1980, 430), (1200, 430), (1200, 715)]],
           saltos=[(1200, 440), (1200, 480), (1200, 540), (1200, 590), (1200, 630)])

# 15 (compartida): Monitoreo y Mantenimientos -> Notificacion
d.interfaz((1700, 155, "IPublishAlert", "start"),
           proveedor=[(1560, 175), (1650, 175)],
           consumidores=[[(2100, 280), (2100, 175), (1650, 175)],
                         [(2260, 600), (2620, 600), (2620, 110), (1650, 110), (1650, 175)]])

# 20: Vuelos -> Monitoreo
d.interfaz((2595, 704, "IGetAlertsOfMission", "start"),
           proveedor=[(2260, 400), (2580, 400), (2580, 700)],
           consumidores=[[(2260, 1000), (2580, 1000), (2580, 700)]],
           saltos=[(2580, 600)])

# 21: Mantenimientos -> Configuracion
d.interfaz((1620, 1285, "IGetMaintenanceThresholds", "middle"),
           proveedor=[(1580, 1255), (1620, 1255)],
           consumidores=[[(1940, 810), (1940, 900), (1700, 900), (1700, 1255), (1620, 1255)]],
           saltos=[(1700, 1040)])

# 22, 24, 25, 26: Mantenimientos -> Flota
for y, nombre in [(640, "ISendMaintenance"), (690, "IReactivate"),
                  (740, "IReportFault"), (790, "IDecommissionDrone")]:
    d.interfaz((1780, y - 12, nombre, "middle"),
               proveedor=[(1580, y), (1780, y)],
               consumidores=[[(1980, y), (1780, y)]])

# 27: Mantenimientos -> Vuelos
d.interfaz((2065, 879, "IResetHistory", "end"),
           proveedor=[(2080, 940), (2080, 875)],
           consumidores=[[(2080, 810), (2080, 875)]])

# 28: Validacion de Rutas -> proveedor externo
d.interfaz((1025, 854, "IGetRestrictedZones", "end"),
           proveedor=[(1040, 880), (1040, 850)],
           consumidores=[[(1040, 770), (1040, 850)]],
           saltos=[(1040, 820)])

# ===================================================================
# C. Eventos
# ===================================================================

# E1: Misiones -> Vuelos
d.interfaz((1340, 1510, ["IMissionCompleted", "«event»"], "middle"),
           proveedor=[(620, 840), (680, 840), (680, 1480), (1340, 1480)],
           consumidores=[[(2160, 1090), (2160, 1480), (1340, 1480)]],
           saltos=[(680, 1070)])

# E2: Vuelos -> Mantenimientos
d.interfaz((2155, 879, ["IHistoryUpdated", "«event»"], "start"),
           proveedor=[(2140, 940), (2140, 875)],
           consumidores=[[(2140, 810), (2140, 875)]])

# E3: Flota -> Misiones
d.interfaz((1000, 405, ["IDroneAvailable", "«event»"], "middle"),
           proveedor=[(1460, 560), (1460, 440), (1000, 440)],
           consumidores=[[(600, 450), (600, 440), (1000, 440)]])

d.guardar(sys.argv[1])
print("generado")
