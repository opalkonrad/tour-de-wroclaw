import argparse
from pathlib import Path

from graph.graph_generator import GraphGenerator


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Shapefile extractor.')
    parser.add_argument('--osm-lines',
                        type=str,
                        help='path to OpenStreetMap shapefile (lines)')
    parser.add_argument('--osm-points',
                        type=str,
                        help='path to OpenStreetMap shapefile (points)')
    parser.add_argument('--official',
                        type=str,
                        help='path to official cycle paths shapefile')
    parser.add_argument('--output',
                        type=str,
                        default="./data",
                        help='path to output directory')
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    output_path = Path(args.output)

    graph_generator = GraphGenerator()

    if args.osm_lines:
        osm_graph = graph_generator.create_from_osm_lines(args.osm_lines)
        graph_generator.show_graph(osm_graph)
        graph_generator.save_graph(osm_graph, output_path / 'roads')

    if args.osm_points:
        attractions = graph_generator.get_attractions(args.osm_points)
        graph_generator.show_graph(attractions)
        graph_generator.save_graph(attractions, output_path / 'attractions')

    if args.official:
        official_graph = graph_generator.create_from_official(args.official)
        graph_generator.show_graph(official_graph)
        graph_generator.save_graph(official_graph, output_path / 'official')
