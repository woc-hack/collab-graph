import io
import itertools
import re

from frontend.data_formatting.gexf_format import start_nodes, write_node, finish_nodes, start_edges, write_edge, \
    finish_edges, start, finish
from frontend.data_formatting.graph_structures import Node, Edge


def format_string(s: str):
    return re.sub(r'\W', r'', s.replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("&", "&amp;").strip("\n"))


a2p_dict = {}
a2i_dict = {}
# for each project stores list of authors with its index for faster computation
p2a2i_dict = {}

authors_len = 0
projects_len = 0
with io.open("../data/sample-data.txt", encoding="latin-1") as f:
    for line in f:
        project, author = line.split(";")
        author = format_string(author)
        project = format_string(project)

        print(f"reading data, project: {project}, author {author}")
        if author in a2p_dict:
            a2p_dict[author].append(project)
        else:
            a2p_dict[author] = [project]

        if author not in a2i_dict:
            a2i_dict[author] = len(a2i_dict)
        author_index = a2i_dict[author]
        if project in p2a2i_dict:
            p2a2i_dict[project].append((author, author_index))
        else:
            p2a2i_dict[project] = [(author, author_index)]

assert len(a2i_dict) == len(a2p_dict)

nodes = []
edges = []
authors = [*a2i_dict]
for i, author in enumerate(authors):
    print(f"filling graph: i = {i}")
    nodes.append(Node(str(i), author, len(a2p_dict[author]), author))

    adj_authors = set(itertools.chain(*[p2a2i_dict[p] for p in a2p_dict[author]]))
    for adj_author, j in adj_authors:
        if j > i:
            common_projects = list(set(a2p_dict[author]) & set(a2p_dict[adj_author]))
            if len(common_projects) > 0:
                edges.append(Edge(str(len(edges)), str(i), str(j), " ".join(common_projects), len(common_projects)))

with io.open("../data/sample-data.gexf", encoding="latin-1", mode="w+") as f:
    start(f)
    start_nodes(f)
    for node in nodes:
        print(f"writing node: {node.id}")
        write_node(f, node)
    finish_nodes(f)
    start_edges(f)
    for edge in edges:
        print(f"writing edge: {edge.id}")
        write_edge(f, edge)
    finish_edges(f)
    finish(f)

