from enum import Enum


class BikepathType(str, Enum):
    WITHPEDESTRIANS = "droga dla pieszych i rowerów"
    FULL = "droga dla rowerów"
    CONTRALANE = "kontrapas"
    CONTRAFLOW = "kontraruch"
    CANRIDE = "możliwość przejazdu"
    WBUS = "pas BUS + ROWER"
    BIKELANE = "pas ruchu dla rowerów"
    CALMFLOW = "strefa ruchu uspokojonego 20 i 30 km/h"
    ONLEVEES = "trasa na wałach"
    THRUPARK = "trasa przez park"
    ROADLINK = "łącznik drogow"
