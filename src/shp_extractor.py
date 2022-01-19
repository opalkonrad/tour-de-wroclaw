import argparse
from pathlib import Path

from algorithm.join import join_attractions
from graph import GraphGenerator


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Shapefile extractor.")
    parser.add_argument("--osm-lines", type=Path, help="path to OpenStreetMap shapefile (lines)")
    parser.add_argument("--osm-points", type=Path, help="path to OpenStreetMap shapefile (points)")
    parser.add_argument("--bike-paths", type=Path, help="path to official cycle paths shapefile")
    parser.add_argument("--output", type=Path, default="data", help="path to output directory")
    parser.add_argument("--merge-attractions", dest="merge", action="store_true", help="add attractions to graphs")
    parser.set_defaults(merge=False)
    parser.add_argument("--show-graphs", dest="show", action="store_true", help="show graphs")
    parser.set_defaults(show=False)
    parser.add_argument("--verbose", action="store_true", help="verbose output")
    parser.set_defaults(verbose=False)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()

    graph_generator = GraphGenerator()

    Path(args.output).mkdir(parents=True, exist_ok=True)

    if args.osm_lines:
        if args.verbose:
            print("Creating roads graph from lines shapefile.")
        roads = graph_generator.create_from_osm_lines(args.osm_lines)
        if args.show:
            graph_generator.show_graph(roads)
        if args.verbose:
            print("Saving graph with roads.")
        graph_generator.save_graph(roads, args.output / "roads.pickle")
    else:
        if args.verbose:
            print("Reading roads graph.")
        roads = graph_generator.read_graph(args.output / "roads.pickle")

    if args.osm_points:
        if args.verbose:
            print("Creating attractions graph from points shapefile.")
        attractions = graph_generator.create_from_osm_points(args.osm_points)
        if args.show:
            graph_generator.show_graph(attractions)
        if args.verbose:
            print("Saving graph with attractions.")
        graph_generator.save_graph(attractions, args.output / "attractions.pickle")
    else:
        if args.verbose:
            print("Reading attractions graph.")
        attractions = graph_generator.read_graph(args.output / "attractions.pickle")

    if args.bike_paths:
        if args.verbose:
            print("Creating bike paths graph from bike paths shapefile.")
        bike_paths = graph_generator.create_from_bike_paths(args.bike_paths)
        if args.show:
            graph_generator.show_graph(bike_paths)
        if args.verbose:
            print("Saving graph with bike paths.")
        graph_generator.save_graph(bike_paths, args.output / "bike_paths.pickle")
    else:
        if args.verbose:
            print("Reading bike paths graph.")
        bike_paths = graph_generator.read_graph(args.output / "bike_paths.pickle")

    if args.merge:
        if args.verbose:
            print("Merging graphs. This may take a while...")
        roads_w_attractions = join_attractions(roads, attractions)
        bike_paths_w_attractions = join_attractions(bike_paths, attractions)

        if args.verbose:
            print("Saving merged graphs.")
        graph_generator.save_graph(roads_w_attractions, args.output / "roads_w_attractions.pickle")
        graph_generator.save_graph(bike_paths_w_attractions, args.output / "bike_paths_w_attractions.pickle")
