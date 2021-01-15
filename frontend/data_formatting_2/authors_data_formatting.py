import io
import re
import sys
import time

sys.path.append("..")

from frontend.data_formatting_2.gexf_format import start_nodes, write_node, finish_nodes, start_edges, write_edge, \
    finish_edges, start, finish
from frontend.data_formatting_2.graph_structures import Node


def format_string(s):
    return re.sub(r'[^\x00-\x7F]+', ' ',
                  s.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("&", "&amp;").strip("\n"))


def main(in_path, out_path, min_authors_n):
    with io.open(in_path, encoding="latin-1") as f:
        print "start filling graph"

        # For each project stores a list of authors
        p2as = {}
        # For each author stores a list of projects
        a2ps = {}
        lines = f.readlines()
        lines_n = len(lines)
        for i, line in enumerate(lines):
            try:
                author, project = line.split(";")
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

    # Create nodes from projects that meet the requirement of the min authors number
    node_i = 0
    nodes = []
    for p, authors in p2as.items():
        if len(authors) >= min_authors_n:
            node = Node(node_i, p, len(authors), p)
            nodes.append(node)
            node_i += 1

    # Filter a2ps, removing the projects with insufficient amount of authors
    p2id = {node.project : node.id for node in nodes}
    a2ps = {a: [p for p in projects if p in p2id] for a, projects in a2ps.items()}

    # Create edges where its size is the number of common authors between two projects
    e2size = {}
    authors_n = len(a2ps)
    print "nodes", len(nodes)

    for i, (author, projects) in enumerate(a2ps.items()):
        print "filling edges: ", i, "/", authors_n
        projects_n = len(projects)
        for j, p1 in enumerate(projects):
            print "project: ", j, "/", projects_n
            id1 = p2id[p1]
            for p2 in projects[j+1:]:
                id2 = p2id[p2]
                if id1 != id2:
                    if id1 < id2:
                        edge = (nodes[id1], nodes[id2])
                    else:
                        edge = (nodes[id2], nodes[id1])

                    if edge not in e2size:
                        e2size[edge] = 1
                    else:
                        e2size[edge] += 1


    print "nodes", len(nodes)
    print "edges", len(e2size)

    # Write graph in .gexf format
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


