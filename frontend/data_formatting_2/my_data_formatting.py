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
    prev_project = ""
    a2ps = {}
    nodes_n = 0

    p2a_dict = {}

    # manager = mp.Manager()
    # ns = manager.Namespace()
    # ns.edges = []

    with io.open(in_path, encoding="latin-1") as f:
        print "start filling graph"

        try:
            projs = {}
            a2ps = {}
            lines = f.readlines()
            lines_n = len(lines)
            for i, line in enumerate(lines):
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
            pass

    nodes = [Node(i, p, len(auth), p) for i, (p, auth) in enumerate(projs.items()) \
             if len(auth) >= min_authors_n]
    proj_inds = {node.project:node.id for node in nodes}
    a2ps = {a: [p for p in projects if p in proj_inds] for a, projects in a2ps}



                # if i == 0:
                #     project, author = line.split(";")
                #     author = format_string(author)
                #     prev_project = format_string(project)
                #
                #     cur_authors_n = 1
                #     cur_project_authors = [author]
                #     continue
                # else:
                #     project, author = line.split(";")
                #     author = format_string(author)
                #     project = format_string(project)
                #     if project != prev_project:
                #         # finish processing prev project
                #         if cur_authors_n >= min_authors_n:
                #             node = Node(nodes_n, prev_project, cur_authors_n, prev_project)
                #             nodes.append(node)
                #             nodes_n += 1
                #             for a in cur_project_authors:
                #                 if a in a2ps:
                #                     a2ps[a].append(node)
                #                 else:
                #                     a2ps[a] = [node]
                #
                #         cur_authors_n = 1
                #         cur_project_authors = [author]
                #         prev_project = project
                #     else:
                #         cur_authors_n += 1
                #         cur_project_authors.append(author)

            # finish processing prev project
            # if cur_authors_n >= min_authors_n:
            #     node = Node(nodes_n, prev_project, cur_authors_n, prev_project)
            #     nodes.append(node)
            #     nodes_n += 1
            #     for author in cur_project_authors:
            #         if author in a2ps:
            #             a2ps[author].append(node)
            #         else:
            #             a2ps[author] = [node]

    e2size = {}
    edges_n = 0

    authors_n = len(a2ps)

    print "nodes", len(nodes)


    for i, (author, projects) in enumerate(a2ps.items()):
        print "filling edges: ", i, "/", authors_n
        for i, p1 in enumerate(projects):
            i1 = proj_inds[p1]
            for p2 in projects[i+1:]:
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
