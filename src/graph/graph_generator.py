import re
from abc import ABC, abstractmethod
from typing import Tuple

import fiona
import matplotlib.pyplot as plt
import networkx as nx

from src.utils import convert_coords_list, haversine, in_scope


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
        accepted_highways = {
            "secondary",
            "tertiary",
            "unclassified",
            "residential",
            "living_street",
            "service",
            "pedestrian",
            "track",
            "road",
            "busway",
            "footway",
            "bridleway",
            "path",
            "cycleway",
        }
        cur_id = 1
        coordinates_points = {}
        graph = nx.Graph()
        file = fiona.open(path, "r")

        for feature in file:
            highway_type = feature["properties"]["highway"]
            if highway_type in accepted_highways:
                coords = feature["geometry"]["coordinates"] if feature["geometry"] else []
                for pos in coords:
                    if pos not in coordinates_points:
                        coordinates_points[pos] = cur_id
                        cur_id += 1
                        graph.add_node(coordinates_points[pos], pos=pos)
                for start, end in zip(coords, coords[1:]):
                    edge_len = haversine(*start, *end)
                    graph.add_edge(coordinates_points[start], coordinates_points[end], length=edge_len)

        return graph

    def create_from_official(self, path: str) -> nx.Graph:
        cur_id = 1
        coordinates_points = {}
        graph = nx.Graph()
        file = fiona.open(path, "r")

        for feature in file:
            coords = feature["geometry"]["coordinates"] if feature["geometry"] else []
            coords = convert_coords_list(coords)
            for pos in coords:
                if pos not in coordinates_points:
                    coordinates_points[pos] = cur_id
                    cur_id += 1
                    graph.add_node(coordinates_points[pos], pos=pos)
            for start, end in zip(coords, coords[1:]):
                edge_len = haversine(*start, *end)
                try:
                    path_type = feature["properties"]["TYP"]
                except KeyError:
                    path_type = ""
                try:
                    path_direction = float(feature["properties"]["KIERUNEK"])
                except KeyError:
                    path_direction = 0.0
                graph.add_edge(
                    coordinates_points[start],
                    coordinates_points[end],
                    length=edge_len,
                    type=path_type,
                    direction=path_direction,
                )

        return graph

    def get_attractions(self, path: str) -> nx.Graph:
        accepted_attractions = "attraction|aquarium|artwork|gallery|museum|picnic_site|theme_park|viewpoint|zoo"
        cur_id = 1
        coordinates_points = {}
        graph = nx.Graph()
        file = fiona.open(path, "r")

        for feature in file:
            other_tags = feature["properties"]["other_tags"]
            if other_tags:
                attraction = re.search(f'"tourism"=>"({accepted_attractions})"', other_tags)
                if attraction:
                    coords = feature["geometry"]["coordinates"] if feature["geometry"] else None
                    if coords not in coordinates_points and in_scope(coords):
                        coordinates_points[coords] = cur_id
                        cur_id += 1
                        graph.add_node(
                            coordinates_points[coords],
                            pos=coords,
                            name=feature["properties"]["name"],
                            id=coordinates_points[coords],
                        )
        return graph

    def read_graph(self, path: str) -> nx.Graph:
        return nx.read_gpickle(path)

    def save_graph(self, graph: nx.Graph, path: str) -> None:
        nx.write_gpickle(graph, path)

    @staticmethod
    def show_graph(graph: nx.Graph) -> None:
        pos = nx.get_node_attributes(graph, "pos")
        nx.draw(graph, pos)
        plt.show()
