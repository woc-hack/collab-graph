import io
import itertools
import re
import sys
import multiprocessing as mp
import time
from functools import partial

sys.path.append("..")

from frontend.data_formatting_2.gexf_format import start_nodes, write_node, finish_nodes, start_edges, write_edge, \
    finish_edges, start, finish
from frontend.data_formatting_2.graph_structures import Node, Edge


def format_string(s):
    return re.sub(r'\W', r'',
                  s.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("&", "&amp;").strip("\n"))



def main(in_path, out_path, min_authors_n):
    nodes = []
    edges = []
    prev_project = ""
    nodes_n = 0
    edges_n = 0

    p2a_dict = {}

    # manager = mp.Manager()
    # ns = manager.Namespace()
    # ns.edges = []

    with io.open(in_path, encoding="latin-1") as f:
        print "start filling graph"

        for i, line in enumerate(f):
            if i == 0:
                project, author = line.split(";")
                author = format_string(author)
                prev_project = format_string(project)

                cur_authors_n = 1
                cur_project_authors = [author]
                continue
            try:
                project, author = line.split(";")
                author = format_string(author)
                project = format_string(project)
                if project != prev_project:
                    # finish processing prev project
                    if cur_authors_n >= min_authors_n:
                        p2a_dict[prev_project] = set(cur_project_authors)

                        for node in nodes:
                            common_authors_n = len(p2a_dict[node.project] & p2a_dict[prev_project])
                            if common_authors_n > 0:
                                edge = Edge(edges_n, node.id, nodes_n, common_authors_n, common_authors_n)
                                edges.append(edge)
                                edges_n += 1

                        nodes.append(Node(nodes_n, prev_project, cur_authors_n, prev_project))
                        nodes_n += 1
                        print(nodes_n)

                    cur_authors_n = 1
                    cur_project_authors = [author]
                    prev_project = project
                else:
                    cur_authors_n += 1
                    cur_project_authors.append(author)
            except ValueError:
                pass


    print "nodes", nodes_n
    print "edges", edges_n


    with io.open(out_path, encoding="latin-1", mode="w+") as f:
        print("start writing graph")
        start(f)
        start_nodes(f)
        for node in nodes:
            write_node(f, node)
        finish_nodes(f)
        start_edges(f)
        edges_n = 0
        for edge in edges:
            write_edge(f, edge)
        finish_edges(f)
        finish(f)


if __name__ == '__main__':
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    min_authors = sys.argv[3]
    # in_path = "../data/sample-data.txt"
    # out_path = "../data/filtered_data_3.gexf"
    # min_authors = 3
    start_time = time.time()
    main(in_path, out_path, int(min_authors))
    end_time = time.time()
    print(end_time - start_time)

# ../data/sample-data.txt
# ../data/filtered-data.gexf

#  2:
# 5550
# 102456
#  3:
#  5550
# 102428vf
