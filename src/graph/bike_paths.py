from enum import Enum


class BikePathType(str, Enum):
    BIKELANE = "pas ruchu dla rowerów"
    CALMFLOW = "strefa ruchu uspokojonego 20 i 30 km/h"
    CANRIDE = "możliwość przejazdu"
    CONTRAFLOW = "kontraruch"
    CONTRALANE = "kontrapas"
    FULL = "droga dla rowerów"
    ONLEVEES = "trasa na wałach"
    ROADLINK = "łącznik drogow"
    THRUPARK = "trasa przez park"
    WBUS = "pas BUS + ROWER"
    WITHPEDESTRIANS = "droga dla pieszych i rowerów"


FULL_BIKE_PATH = [
    BikePathType.BIKELANE,
    BikePathType.CALMFLOW,
    BikePathType.CONTRAFLOW,
    BikePathType.CONTRALANE,
    BikePathType.FULL,
    BikePathType.ONLEVEES,
    BikePathType.THRUPARK,
    BikePathType.WBUS,
    BikePathType.WITHPEDESTRIANS
]
