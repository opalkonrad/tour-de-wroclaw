from typing import Callable, List

import networkx as nx
from networkx.algorithms.shortest_paths.astar import astar_path
from networkx.classes.function import path_weight

from src.utils import haversine, PENALTY_FACTOR


def get_heur(network: nx.Graph) -> Callable:
    def heur_distance(v1, v2):
        vv1 = network.nodes[v1]["pos"]
        vv2 = network.nodes[v2]["pos"]
        return haversine(*vv1, *vv2)
    return heur_distance


def find_path(network: nx.Graph, start: int, end: int) -> List[int]:
    heur_distance = get_heur(network)
    shortest_path = astar_path(network, start, end, heuristic=heur_distance, weight="length")
    return shortest_path


def path_len(network: nx.Graph, path: List[int]) -> float:
    original_len = path_weight(network, path, weight="length")
    penalty = path_weight(network, path[:2], weight="length") + path_weight(network, path[-2:], weight="length")
    return original_len + (PENALTY_FACTOR - 1) * penalty
