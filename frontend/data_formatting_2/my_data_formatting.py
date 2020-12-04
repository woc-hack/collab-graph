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
    a2ps = {}

    with io.open(in_path, encoding="latin-1") as f:
        print "start filling graph"

        projs = {}
        a2ps = {}
        lines = f.readlines()
        lines_n = len(lines)
        for i, line in enumerate(lines):
            try:
                project, author = line.split(";")
                project = format_string(project)
                author = format_string(author)
                if project in projs:
                    projs[project].append(author)
                else:
                    projs[project] = [author]
                if author in a2ps:
                    a2ps[author].append(project)
                else:
                    a2ps[author] = [project]

                if i % 10000 == 0:
                    print(i, lines_n)
            except ValueError:
                print("error")
                pass

    node_i = 0
    nodes = []
    for p, auth in projs.items():
        if len(auth) >= min_authors_n:
            node = Node(node_i, p, len(auth), p)
            nodes.append(node)
            node_i += 1


    # nodes = [Node(i, p, len(auth), p) for i, (p, auth) in enumerate(projs.items()) \
    #          if len(auth) >= min_authors_n]

    proj_inds = {node.project:node.id for node in nodes}
    a2ps = {a: [p for p in projects if p in proj_inds] for a, projects in a2ps.items()}

    e2size = {}
    authors_n = len(a2ps)
    print "nodes", len(nodes)

    for i, (author, projects) in enumerate(a2ps.items()):
        print "filling edges: ", i, "/", authors_n
        projects_n = len(projects)
        for j, p1 in enumerate(projects):
            print "project: ", j, "/", projects_n
            i1 = proj_inds[p1]
            for p2 in projects[j+1:]:
                i2 = proj_inds[p2]
                if i1 != i2:
                    if i1 < i2:
                        e = (nodes[i1], nodes[i2])
                    else:
                        e = (nodes[i2], nodes[i1])

                    if e not in e2size:
                        e2size[e] = 1
                    else:
                        e2size[e] += 1



    print "nodes", len(nodes)
    print "edges", len(e2size)


    with io.open(out_path, encoding="latin-1", mode="w+") as f:
        print("start writing graph")
        start(f)
        start_nodes(f)
        for node in nodes:
            write_node(f, node)
        finish_nodes(f)
        start_edges(f)
        for i, ((p1, p2), size) in enumerate(e2size.items()):
            write_edge(f, i, p1.id, p2.id, size)
        finish_edges(f)
        finish(f)


if __name__ == '__main__':
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    min_authors = sys.argv[3]
    # in_path = "/home/elena/p2a_table"
    # out_path = "../data/filtered_data_10_easy.gexf"
    # min_authors = 1
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
