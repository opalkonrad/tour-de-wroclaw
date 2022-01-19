from typing import Any, Dict, List, Tuple
import networkx as nx

from src.utils import haversine, Vertex


def closest_vertex(v1: Tuple[float, float], vertices: List[Vertex]) -> Tuple[Vertex, float]:
    closest = None
    min_distance = 10e9
    for v in vertices:
        distance = haversine(*v1, *v[1]["pos"])
        if distance < min_distance:
            closest = v
            min_distance = distance
    
    return closest, min_distance


def add_attraction_to_network(attraction: Vertex, new_id: int, closest: Vertex, distance: float, network: nx.Graph) -> None:
    network.add_node(new_id, **attraction[1])
    network.add_edge(new_id, closest[0], length=distance)


def join_attractions(network: nx.Graph, attractions: nx.Graph) -> nx.Graph:
    network_nodes = list(network.nodes.items())
    to_add: List[Tuple[Vertex, Vertex, float]] = []

    for attraction in attractions.nodes.items():
        a_coords = attraction[1]["pos"]
        closest, distance = closest_vertex(a_coords, network_nodes)
        to_add.append((attraction, closest, distance))
        
    vid = max(network_nodes, key=lambda x: x[0])[0] + 1
    for attraction_v, closest_v, distance in to_add:
        add_attraction_to_network(attraction_v, vid, closest_v, distance, network)
        vid = vid + 1
    
    return network
