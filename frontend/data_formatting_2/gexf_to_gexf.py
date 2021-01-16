import re
import io
import sys
import time

sys.path.append("..")

from frontend.data_formatting_2.gexf_format import start, start_nodes, write_node, finish_nodes, start_edges, write_edge, \
    finish_edges, finish
from frontend.data_formatting_2.graph_structures import Node, Edge


def main(in_path, out_path, min_node_size, min_edge_size):
    prev_nodes_n = 0
    prev_edges_n = 0

    id2n = {}

    nodes = []
    edges = []

    n2edge_count = {}

    with io.open(in_path) as f:
        lines = f.readlines()
        lines_n = len(lines)
        for i, line in enumerate(lines):
            if i % 100000 == 0:
                print(i, lines_n)
            node_search = re.search("<node id=\"(\d*)\" label=\"(.*)\" size=\"(.*)\"/>", line, re.IGNORECASE)
            if node_search:
                prev_nodes_n += 1
                node = Node(node_search.group(1), node_search.group(2), float(node_search.group(3)), node_search.group(2))
                # filter out all nodes that don't meet the size requirements
                if node.size >= min_node_size:
                    nodes.append(node)
                    id2n[node.id] = node

            edge_search = re.search(
                "<edge id=\"(\d*)\" source=\"(\d*)\" target=\"(\d*)\" label=\"(.*)\" weight=\"(.*)\"/>",
                line, re.IGNORECASE)
            # by the time we process an edge all nodes should be already processed
            if edge_search:
                prev_edges_n += 1
                edge = Edge(edge_search.group(1), edge_search.group(2), edge_search.group(3), edge_search.group(4),
                            float(edge_search.group(5)))

                s_node = id2n.get(edge.source_node_id)
                t_node = id2n.get(edge.target_node_id)
                if s_node is not None and t_node is not None:
                    edges.append(edge)

                    if s_node not in n2edge_count:
                        n2edge_count[s_node] = 1
                    else:
                        n2edge_count[s_node] += 1

                    if t_node not in n2edge_count:
                        n2edge_count[t_node] = 1
                    else:
                        n2edge_count[t_node] += 1

    filtered_edges = []
    edges_n = len(edges)
    print(len(n2edge_count))

    # filter out all edges that don't meet the size requirements
    for i, edge in enumerate(edges):
        print "filtering edges: ", i, "/", edges_n
        if edge.size >= min_edge_size:
            filtered_edges.append(edge)
        else:
            s_node = id2n.get(edge.source_node_id)
            t_node = id2n.get(edge.target_node_id)

            n2edge_count[s_node] -= 1
            n2edge_count[t_node] -= 1

            if n2edge_count[s_node] == 0:
                del n2edge_count[s_node]
                

            if n2edge_count[t_node] == 0:
                del n2edge_count[t_node]




    nodes_n = len(n2edge_count)
    edges_n = len(filtered_edges)

    print nodes_n, edges_n


    with io.open(out_path, "w+") as f:
        print("start writing graph")
        start(f)
        start_nodes(f)
        for i, (node, edge_count) in enumerate(n2edge_count.items()):
            print "writing nodes: ", i, "/",  nodes_n
            write_node(f, node)
        finish_nodes(f)
        start_edges(f)
        for i, edge in enumerate(filtered_edges):
            print"writing edges: ", i, "/", edges_n
            write_edge(f, edge.id, edge.source_node_id, edge.target_node_id, edge.size)
        finish_edges(f)
        finish(f)

    print "was (nodes/edges): ", prev_nodes_n, "/", prev_edges_n, ", now: ", nodes_n, "/", edges_n


if __name__ == '__main__':
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    min_node_size = sys.argv[3]
    min_edge_size = sys.argv[4]
    start_time = time.time()
    main(in_path, out_path, int(min_node_size), int(min_edge_size))
    end_time = time.time()
    print(end_time - start_time)





