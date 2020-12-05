import re
import io
import sys
import time

sys.path.append("..")

from frontend.data_formatting_2.gexf_format import start, start_nodes, write_node, finish_nodes, start_edges, write_edge, \
    finish_edges, finish
from frontend.data_formatting_2.graph_structures import Node, Edge


def main(in_path, out_path, min_authors):
    id2n = {}

    nodes = []
    edges = []

    with io.open(in_path) as f:
        lines = f.readlines()
        lines_n = len(lines)
        for i, line in enumerate(lines):
            if i % 100000 == 0:
                print(i, lines_n)
            node_search = re.search("<node id=\"(\d*)\" label=\"(.*)\" size=\"(.*)\"/>", line, re.IGNORECASE)
            if node_search:
                node = Node(node_search.group(1), node_search.group(2), float(node_search.group(3)), node_search.group(2))
                # filter out all nodes that don't meet the size requirements
                if node.size >= min_authors:
                    nodes.append(node)
                    id2n[node.id] = node

            edge_search = re.search(
                "<edge id=\"(\d*)\" source=\"(\d*)\" target=\"(\d*)\" label=\"(.*)\" weight=\"(.*)\"/>",
                line, re.IGNORECASE)
            # by the time we process an edge all nodes should be already processed
            if edge_search:
                edge = Edge(edge_search.group(1), edge_search.group(2), edge_search.group(3), edge_search.group(4),
                            float(edge_search.group(5)))
                if edge.source_node_id in id2n and edge.target_node_id in id2n:
                    edges.append(edge)

    print(len(nodes))
    print(len(edges))

    with io.open(out_path, "w+") as f:
        print("start writing graph")
        start(f)
        start_nodes(f)
        for node in nodes:
            write_node(f, node)
        finish_nodes(f)
        start_edges(f)
        for edge in edges:
            write_edge(f, edge.id, edge.source_node_id, edge.target_node_id, edge.size)
        finish_edges(f)
        finish(f)


if __name__ == '__main__':
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    min_authors = sys.argv[3]
    start_time = time.time()
    main(in_path, out_path, int(min_authors))
    end_time = time.time()
    print(end_time - start_time)





