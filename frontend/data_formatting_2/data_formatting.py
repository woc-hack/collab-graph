import io
import itertools
import re
import sys

sys.path.append("..")

from frontend.data_formatting_2.gexf_format import start_nodes, write_node, finish_nodes, start_edges, write_edge, \
    finish_edges, start, finish
from frontend.data_formatting_2.graph_structures import Node, Edge


def format_string(s):
    return re.sub(r'\W', r'',
                  s.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("&", "&amp;").strip("\n"))


def main(in_path, out_path, min_authors):
    p2i2a_dict = {}
    p2i_dict = {}
    # for each project stores list of authors with its index for faster computation
    a2p2i_dict = {}

    with io.open(in_path, encoding="latin-1") as f:
        print "start filling graph"
        for line in f:
            try:
                project, author = line.split(";")
                author = format_string(author)
                project = format_string(project)

                if project not in p2i_dict:
                    p2i_dict[project] = len(p2i_dict)
                project_index = p2i_dict[project]

                p2i = (project, project_index)

                if p2i in p2i2a_dict:
                    p2i2a_dict[p2i].append(author)
                else:
                    p2i2a_dict[p2i] = [author]

                if author in a2p2i_dict:
                    a2p2i_dict[author].append(p2i)
                else:
                    a2p2i_dict[author] = [p2i]
            except ValueError:
                pass

    assert len(p2i_dict) == len(p2i2a_dict)

    nodes = []
    edges = []
    filtered_p2a_dict = {project: authors for project, authors in p2i2a_dict.items() if len(authors) >= min_authors}
    print "before filtering ", len(p2i2a_dict), "after filtering ", len(filtered_p2a_dict)

    projects = list(filtered_p2a_dict.keys())

    for en, (project, i) in enumerate(projects):
        if en % 1000 == 0:
            print en, len(projects)
        project_authors = filtered_p2a_dict[(project, i)]
        nodes.append(Node(str(i), project, len(project_authors), project))

        adj_projects = set(itertools.chain(*[a2p2i_dict[a] for a in project_authors])) & set(filtered_p2a_dict.keys())
        for adj_project, j in adj_projects:
            if j > i:
                common_projects = list(set(project_authors) & set(filtered_p2a_dict[(adj_project, j)]))
                if len(common_projects) > 0:
                    edges.append(Edge(str(len(edges)), str(i), str(j), " ".join(common_projects), len(common_projects)))

    print "nodes", len(nodes)
    print "edges", len(edges)

    with io.open(out_path, encoding="latin-1", mode="w+") as f:
        print("start writing graph")
        start(f)
        start_nodes(f)
        for node in nodes:
            write_node(f, node)
        finish_nodes(f)
        start_edges(f)
        for edge in edges:
            write_edge(f, edge)
        finish_edges(f)
        finish(f)


if __name__ == '__main__':
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    min_authors = sys.argv[3]
    main(in_path, out_path, int(min_authors))

# ../data/sample-data.txt
# ../data/filtered-data.gexf

#  2:
# 5550
# 102456
#  3:
#  5550
# 102428vf
