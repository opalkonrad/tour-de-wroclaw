from distutils.log import warn
from typing import List, Optional

import networkx as nx

from src.graph.bike_paths import BikePathType


def filter_bike_paths(
    network: nx.Graph, whitelist: Optional[List[BikePathType]] = None, blacklist: Optional[List[BikePathType]] = None
):
    if (whitelist is None and blacklist is None) or (whitelist is not None and blacklist is not None):
        warn("To filter bike paths pass whitelist xor blacklist")

    network_copy = network.copy()
    to_delete = []
    if whitelist is not None:
        for edge, attrib in network_copy.edges.items():
            if attrib.get("type") in whitelist or attrib.get("type") is None:
                continue
            to_delete.append(edge)
    else:
        for edge, attrib in network_copy.edges.items():
            if attrib.get("type") in blacklist:
                to_delete.append(edge)
    network_copy.remove_edges_from(to_delete)

    return network_copy
