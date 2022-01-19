import pytest
import networkx as nx

from src.algorithm.filter_graphs import filter_bike_paths
from src.graph.bike_paths import BikePathType, FULL_BIKE_PATH


@pytest.fixture
def sample_bike_path_graph():
    graph = nx.Graph()
    graph.add_nodes_from(list(range(1, 13)))
    graph.add_edge(1, 2, length=0.1, type="droga dla pieszych i rowerów", direction=2.0)
    graph.add_edge(2, 3, length=0.1, type="droga dla rowerów", direction=2.0)
    graph.add_edge(3, 4, length=0.1, type="kontrapas", direction=2.0)
    graph.add_edge(4, 5, length=0.1, type="kontraruch", direction=2.0)
    graph.add_edge(5, 6, length=0.1, type="możliwość przejazdu", direction=2.0)
    graph.add_edge(6, 7, length=0.1, type="pas BUS + ROWER", direction=2.0)
    graph.add_edge(7, 8, length=0.1, type="pas ruchu dla rowerów", direction=2.0)
    graph.add_edge(8, 9, length=0.1, type="strefa ruchu uspokojonego 20 i 30 km/h", direction=2.0)
    graph.add_edge(9, 10, length=0.1, type="trasa na wałach", direction=2.0)
    graph.add_edge(10, 11, length=0.1, type="trasa przez park", direction=2.0)
    graph.add_edge(11, 12, length=0.1, type="łącznik drogow", direction=2.0)

    return graph


def test_filtering(sample_bike_path_graph):
    expected_edges = [
        (1, 2),
        (2, 3),
        (9, 10),
        (10, 11),
    ]

    filtered = filter_bike_paths(sample_bike_path_graph, whitelist=FULL_BIKE_PATH)

    assert list(filtered.edges.keys()) == expected_edges
    assert list(filtered.nodes.keys()) == list(sample_bike_path_graph.nodes.keys())
