from math import asin, cos, radians, sin, sqrt
from typing import List, Tuple

from pyproj import Transformer

NORTH_LIM = 51.27
SOUTH_LIM = 50.94
WEST_LIM = 16.70
EAST_LIM = 17.38

transformer = Transformer.from_crs("epsg:2177", "epsg:4326")


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
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


def get_perp(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float):
    """************************************************************************************************
    Purpose - X1,Y1,X2,Y2 = Two points representing the ends of the line segment
              X3,Y3 = The offset point
    'Returns - X4,Y4 = Returns the Point on the line perpendicular to the offset or None if no such
                        point exists
    '************************************************************************************************"""
    xx = x2 - x1
    yy = y2 - y1
    shortestlength = ((xx * (x3 - x1)) + (yy * (y3 - y1))) / ((xx * xx) + (yy * yy))
    x4 = x1 + xx * shortestlength
    y4 = y1 + yy * shortestlength
    if x4 < x2 and x4 > x1 and y4 < y2 and y4 > y1:
        return x4, y4
    return None
