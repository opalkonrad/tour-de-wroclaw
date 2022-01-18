import re
from abc import ABC, abstractmethod
from typing import Tuple
from math import radians, cos, sin, asin, sqrt

import fiona
import matplotlib.pyplot as plt
import networkx as nx

NORTH_LIM = 51.27
SOUTH_LIM = 50.94
WEST_LIM = 16.70
EAST_LIM = 17.38


class AbstractGraphGenerator(ABC):
    @abstractmethod
    def create_from_osm_lines(self, path: str) -> nx.Graph:
        return NotImplemented

    @abstractmethod
    def create_from_official(self, path: str) -> nx.Graph:
        return NotImplemented

    @abstractmethod
    def get_attractions(self, path: str) -> nx.Graph:
        return NotImplemented

    @abstractmethod
    def read_graph(self, path: str) -> nx.Graph:
        return NotImplemented

    @abstractmethod
    def save_graph(self, graph: nx.Graph, path: str) -> None:
        pass


class GraphGenerator(AbstractGraphGenerator):
    def __init__(self) -> None:
        pass

    def create_from_osm_lines(self, path: str) -> nx.Graph:
        accepted_highways = {'secondary', 'tertiary', 'unclassified', 'residential', 'living_street', 'service',
                             'pedestrian', 'track', 'road', 'busway', 'footway', 'bridleway', 'path', 'cycleway'}
        cur_id = 1
        coordinates_points = {}
        graph = nx.Graph()
        file = fiona.open(path, 'r')

        for feature in file:
            highway_type = feature['properties']['highway']
            if highway_type in accepted_highways:
                coords = feature['geometry']['coordinates'] if feature['geometry'] else []
                for pos in coords:
                    if pos not in coordinates_points:
                        coordinates_points[pos] = cur_id
                        cur_id += 1
                        graph.add_node(coordinates_points[pos], pos=pos)
                for start, end in zip(coords, coords[1:]):
                    edge_len = GraphGenerator.haversine(*start, *end)
                    graph.add_edge(coordinates_points[start], coordinates_points[end], length=edge_len)
        return graph

    def create_from_official(self, path: str) -> nx.Graph:
        cur_id = 1
        coordinates_points = {}
        graph = nx.Graph()
        file = fiona.open(path, 'r')

        for feature in file:
            coords = feature['geometry']['coordinates'] if feature['geometry'] else []
            for pos in coords:
                if pos not in coordinates_points:
                    coordinates_points[pos] = cur_id
                    cur_id += 1
                    graph.add_node(coordinates_points[pos], pos=pos)
            for start, end in zip(coords, coords[1:]):
                graph.add_edge(coordinates_points[start], coordinates_points[end])
        return graph

    def get_attractions(self, path: str) -> nx.Graph:
        accepted_attractions = 'attraction|aquarium|artwork|gallery|museum|picnic_site|theme_park|viewpoint|zoo'
        cur_id = 1
        coordinates_points = {}
        graph = nx.Graph()
        file = fiona.open(path, 'r')

        for feature in file:
            other_tags = feature['properties']['other_tags']
            if other_tags:
                attraction = re.search(fr'"tourism"=>"({accepted_attractions})"', other_tags)
                if attraction:
                    coords = feature['geometry']['coordinates'] if feature['geometry'] else None
                    if coords not in coordinates_points and GraphGenerator.in_scope(coords):
                        coordinates_points[coords] = cur_id
                        cur_id += 1
                        graph.add_node(coordinates_points[coords], pos=coords, name=feature["properties"]["name"])
        return graph

    def read_graph(self, path: str) -> nx.Graph:
        return nx.read_gpickle(path)

    def save_graph(self, graph: nx.Graph, path: str) -> None:
        nx.write_gpickle(graph, path)

    @staticmethod
    def show_graph(graph: nx.Graph) -> None:
        pos = nx.get_node_attributes(graph, 'pos')
        nx.draw(graph, pos)
        plt.show()
    
    @staticmethod
    def in_scope(coords: Tuple[float, float]) -> bool:
        if coords[0] > EAST_LIM or coords[0] < WEST_LIM:
            return False
        if coords[1] > NORTH_LIM or coords[1] < SOUTH_LIM:
            return False
        return True
    
    @staticmethod
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
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
        return c * r
