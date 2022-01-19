from distutils.log import warn
from typing import List, Optional

import networkx as nx

from src.graph.bike_paths import BikePathType


def filter_bike_paths(
    network: nx.Graph, whitelist: Optional[List[BikePathType]] = None, blacklist: Optional[List[BikePathType]] = None
):
    if (whitelist is None and blacklist is None) or (whitelist is not None and blacklist is not None):
        warn("To filter bike paths pass whitelist xor blacklist")
    pass
