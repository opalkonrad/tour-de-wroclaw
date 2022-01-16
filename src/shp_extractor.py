import argparse

from src.graph.graph_generator import GraphGenerator


parser = argparse.ArgumentParser(description='Shapefile extractor.')
parser.add_argument('--osm-lines',
                    type=str,
                    required=True,
                    help='path to OpenStreetMap shapefile (lines)')
parser.add_argument('--osm-points',
                    type=str,
                    required=True,
                    help='path to OpenStreetMap shapefile (points)')
parser.add_argument('--official',
                    type=str,
                    required=True,
                    help='path to official cycle paths shapefile')

if __name__ == "__main__":
    args = parser.parse_args()
    graph_generator = GraphGenerator()

    osm_graph = graph_generator.create_from_osm_lines(args.osm_lines)
    graph_generator.show_graph(osm_graph)
    graph_generator.save_graph(osm_graph, './osm')

    attractions = graph_generator.get_attractions(args.osm_points)
    graph_generator.show_graph(attractions)
    graph_generator.save_graph(attractions, './attractions')

    official_graph = graph_generator.create_from_official(args.official)
    graph_generator.show_graph(official_graph)
    graph_generator.save_graph(official_graph, './official')
