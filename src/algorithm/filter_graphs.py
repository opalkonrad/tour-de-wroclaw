from distutils.log import warn
from typing import List, Optional
import networkx as nx

from src.graph.bikepaths import BikepathType


def filter_bikepaths(network: nx.Graph, whitelist: Optional[List[BikepathType]] = None, blacklist: Optional[List[BikepathType]] = None):
    if (whitelist is None and blacklist is None) or (whitelist is not None and blacklist is not None):
        warn("To filter bikepaths pass whitelist xor blacklist")
    pass
