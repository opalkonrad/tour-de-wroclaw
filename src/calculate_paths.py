import argparse
import json
import random
from pathlib import Path
from typing import Optional, Tuple

import networkx as nx
from pyrsistent import b

from algorithm.filter_graphs import filter_bike_paths
from algorithm.link_attractions import get_attraction_pairs
from algorithm.search_path import find_path, path_len
from graph import GraphGenerator
from graph.bike_paths import WHITE_LIST
from graph.path_schema import AttractionNode, AttractionsPair, GraphPath, PairsList

SEED = 4


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Shapefile extractor.")
    parser.add_argument(
        "--attractions", type=Path, help="path to attractions pickle", default=Path("./data/attractions.pickle")
    )
    parser.add_argument(
        "--roads", type=Path, help="path to roads pickle", default=Path("./data/roads_w_attractions.pickle")
    )
    parser.add_argument(
        "--bike-paths",
        type=Path,
        help="path to bike paths pickle",
        default=Path("./data/bikepaths_w_attractions.pickle"),
    )
    parser.add_argument("--output", type=Path, help="path to output directory", default=Path("./out"))
    parser.add_argument("--save-period", type=int, help="period in which to save results to json", default=1000)
    parser.add_argument("--n-pairs", type=int, help="number of checked pairs", default=40000)
    return parser


def save(object: PairsList, path: Path, saved_files) -> None:
    with open(path / f"data{saved_files}.json", "w") as f:
        json.dump(object.dict(), f, indent=4, ensure_ascii=False)
    return saved_files + 1


def get_path(attractions: Tuple[AttractionNode, AttractionNode], network: nx.Graph) -> Optional[GraphPath]:
    a1, a2 = attractions
    path_start = list(filter(lambda x: x[1].get("id") == a1.id, list(network.nodes.items())))[0]
    path_end = list(filter(lambda x: x[1].get("id") == a2.id, list(network.nodes.items())))[0]

    try:
        path = find_path(network, start=path_start[0], end=path_end[0])
        length = path_len(network, path)

        return GraphPath(edges=path, length=length)

    except nx.NetworkXNoPath:
        return None


def main(args, graph_generator: GraphGenerator) -> None:
    args.output.mkdir(parents=True, exist_ok=True)

    attractions = graph_generator.read_graph(args.attractions)
    bike_paths = graph_generator.read_graph(args.bike_paths)
    safe_bike_paths = filter_bike_paths(bike_paths, whitelist=WHITE_LIST)
    roads = graph_generator.read_graph(args.roads)

    pairs = get_attraction_pairs(attractions, min_len=1.0)
    random.Random(SEED).shuffle(pairs)

    checked_pairs = PairsList(pairs=[])
    saved_files = 0
    to_save = args.save_period

    for a1, a2, _ in pairs[: args.n_pairs]:
        road_path = get_path((a1, a2), roads)
        bike_path = get_path((a1, a2), bike_paths)
        safe_bike_path = get_path((a1, a2), safe_bike_paths)
        pair_data = AttractionsPair(
            start=a1,
            end=a2,
            other_path=road_path,
            bike_path=bike_path,
            safer_bike_path=safe_bike_path,
        )
        checked_pairs.pairs.append(pair_data)
        if to_save == 0:
            print(f"Saving {saved_files + 1} part")
            saved_files = save(checked_pairs, args.output, saved_files)
            checked_pairs = PairsList(pairs=[])
            to_save = args.save_period
        else:
            to_save = to_save - 1

    save(checked_pairs, args.output, saved_files)


if __name__ == "__main__":
    args = get_parser().parse_args()
    graph_generator = GraphGenerator()

    main(args, graph_generator)
