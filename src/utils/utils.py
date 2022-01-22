from math import asin, cos, radians, sin, sqrt
from typing import Any, Dict, List, Tuple

from pyproj import Transformer

NORTH_LIM = 51.27
SOUTH_LIM = 50.94
WEST_LIM = 16.70
EAST_LIM = 17.38

PENALTY_FACTOR = 2.0

transformer = Transformer.from_crs("epsg:2177", "epsg:4326")

Vertex = Tuple[int, Dict[str, Any]]


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


def convert_epsg(x: float, y: float) -> Tuple[float, float]:
    lon, lat = transformer.transform(y, x)
    return lat, lon


def convert_coords_list(coords: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    return [convert_epsg(x, y) for x, y in coords]


def in_scope(coords: Tuple[float, float]) -> bool:
    if coords[0] > EAST_LIM or coords[0] < WEST_LIM:
        return False
    if coords[1] > NORTH_LIM or coords[1] < SOUTH_LIM:
        return False
    return True
