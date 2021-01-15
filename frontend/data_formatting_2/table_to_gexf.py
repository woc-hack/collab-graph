import io
import re
import sys
import time
from plistlib import Dict

sys.path.append("..")

from frontend.data_formatting_2.gexf_format import start_nodes, write_node, finish_nodes, start_edges, write_edge, \
    finish_edges, start, finish
from frontend.data_formatting_2.graph_structures import Node


def format_string(s):
    return re.sub(r'[^\x00-\x7F]+', ' ',
                  s.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("&", "&amp;").strip("\n"))


def parse_table(table_path):
    print "start parsing table"
    # For each project stores a list of authors
    p2as = {}
    # For each author stores a list of projects
    a2ps = {}
    with io.open(table_path, encoding="latin-1") as f:
        lines = f.readlines()
        lines_n = len(lines)
        for i, line in enumerate(lines):
            try:
                project, author = line.split(";")
                project = format_string(project)
                author = format_string(author)
                if project in p2as:
                    p2as[project].append(author)
                else:
                    p2as[project] = [author]
                if author in a2ps:
                    a2ps[author].append(project)
                else:
                    a2ps[author] = [project]

                if i % 10000 == 0:
                    print(i, lines_n)
            except ValueError:
                print("error")
                pass
    return p2as, a2ps




# Create graph from two dictionaries:
# 1. node to list of related edges
# 2. edge to list of related nodes
# For example, author (as node) to list of their projects and project (as edge) to list of its authors
# min_number restricts the size of the list, related to node
# For example, with min_number = 5 we take into account only authors with len(projects) >= 5
def create_and_write_graph(log, n2edges, e2nodes, min_n, out_file):
    print len(n2edges), len(e2nodes), min_n
    print log, "start creating nodes"
    # Create graph nodes from nodes that meet the requirement of the min authors number
    graph_node_i = 0
    graph_nodes = []
    nodes_len = len(n2edges.items())
    for i, (node, edges) in enumerate(n2edges.items()):
        print log, "filling nodes: ", i, "/", nodes_len
        if len(edges) >= min_n:
            node = Node(graph_node_i, node, len(edges), "")
            graph_nodes.append(node)
            graph_node_i += 1

    print log, "nodes", len(graph_nodes)

    # Filter e2nodes, removing the nodes with insufficient amount of edges (i.e < min_number)
    n2id = {graph_node.label: graph_node.id for graph_node in graph_nodes}
    filtered_e2nodes = {edge: [n for n in nodes if n in n2id] for edge, nodes in e2nodes.items()}

    # Create graph edges where its size is the number of common edges between two nodes
    graph_e2size = {}
    edges_len = len(filtered_e2nodes)

    for i, (edge, nodes) in enumerate(filtered_e2nodes.items()):
        print log, "filling edges: ", i, "/", edges_len
        nodes_len = len(nodes)
        for j, node1 in enumerate(nodes):
            print log, "project: ", j, "/", nodes_len
            id1 = n2id[node1]
            for node2 in nodes[j+1:]:
                id2 = n2id[node2]
                if id1 != id2:
                    if id1 < id2:
                        edge = (graph_nodes[id1], graph_nodes[id2])
                    else:
                        edge = (graph_nodes[id2], graph_nodes[id1])

                    if edge not in graph_e2size:
                        graph_e2size[edge] = 1
                    else:
                        graph_e2size[edge] += 1


    print log, "nodes", len(graph_nodes)
    print log, "edges", len(graph_e2size)

    # Write graph in .gexf format
    with io.open(out_file, encoding="latin-1", mode="w+") as f:
        print log, "start writing graph"
        start(f)
        start_nodes(f)
        for node in graph_nodes:
            write_node(f, node)
        finish_nodes(f)
        start_edges(f)
        for i, ((node1, node2), size) in enumerate(graph_e2size.items()):
            write_edge(f, i, node1.id, node2.id, size)
        finish_edges(f)
        finish(f)


def main(table_path, out_authors_path, out_projects_path, min_authors_n, min_projects_n):
    p2as, a2ps = parse_table(table_path)
    create_and_write_graph("authors as nodes ", a2ps, p2as, min_authors_n, out_authors_path)
    create_and_write_graph("projects as nodes ", p2as, a2ps, min_projects_n, out_projects_path)


if __name__ == '__main__':
    table_path = sys.argv[1]
    out_authors_path = sys.argv[2]
    out_projects_path = sys.argv[3]
    min_authors_number = int(sys.argv[4])
    min_projects_number = int(sys.argv[5])

    start_time = time.time()
    
    main(table_path, out_authors_path, out_projects_path, min_authors_number, min_projects_number)

    end_time = time.time()
    print(end_time - start_time)


