from curses import pair_content
from itertools import combinations
from typing import List, Optional, Tuple
import networkx as nx

from src.graph.path_schema import AttractionNode, AttractionsPair, GraphPath, PairsList
from src.utils import haversine
from .search_path import find_path, path_len


def get_attraction_pairs(network: nx.Graph, min_len: float = 1.0, max_weld_distance: float = 0.1) -> List[Tuple[AttractionNode, AttractionNode, int]]:
    attractions_pairs: List[Tuple[AttractionNode, AttractionNode, int]] = []
    for a1, a2 in combinations(network.nodes.items(), 2):
        an1 = AttractionNode(id=a1[0], name=a1[1].get("name"), pos=a1[1]["pos"])
        an2 = AttractionNode(id=a2[0], name=a2[1].get("name"), pos=a2[1]["pos"])
        if haversine(*an1.pos, *an2.pos) >= min_len:
            attractions_pairs.append((an1, an2, 1))
    
    return attractions_pairs



def check_if_weld(attractions_pairs: List[Tuple[AttractionNode, AttractionNode, int]], new_pair: Tuple[AttractionNode, AttractionNode], max_d: float) -> Optional[int]:
    a1, a2 = new_pair
    coords1 = a1.pos
    coords2 = a2.pos
    old_pair_no = None
    
    for i, pair in enumerate(attractions_pairs):
        a3, a4, _ = pair
        coords3 = a3.pos
        coords4 = a4.pos
        if (
                (haversine(*coords1, *coords3) < max_d and haversine(*coords2, *coords4) < max_d) 
                or 
                (haversine(*coords1, *coords4) < max_d and haversine(*coords2, *coords3) < max_d)
            ):
            old_pair_no = i
            break
    
    return old_pair_no
