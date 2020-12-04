import re
import io

from frontend.data_formatting.gexf_format import start, start_nodes, write_node, finish_nodes, start_edges, write_edge, \
    finish_edges, finish
from frontend.data_formatting.graph_structures import Node, Edge

# node id to node
id2n = {}

nodes = []
edges = []

min = 20


with io.open("../data/filtered_data.gexf") as f:
    for line in f:
        node_search = re.search("<node id=\"(\d*)\" label=\"(.*)\" size=\"(.*)\"/>", line, re.IGNORECASE)
        if node_search:
            node = Node(node_search.group(1), node_search.group(2), float(node_search.group(3)))
            # filter out all nodes that don't meet the size requirements
            if node.size >= min:
                nodes.append(node)
                id2n[node.id] = node

        edge_search = re.search("<edge id=\"(\d*)\" source=\"(\d*)\" target=\"(\d*)\" label=\"(.*)\" weight=\"(.*)\"/>",
                                line, re.IGNORECASE)
        # by the time we process an edge all nodes should be already processed
        if edge_search:
            edge = Edge(edge_search.group(1), edge_search.group(2), edge_search.group(3), edge_search.group(4), float(edge_search.group(5)))
            if edge.source_node_id in id2n and edge.target_node_id in id2n:
                edges.append(edge)


print(len(nodes))
print(len(edges))

with io.open(f"../data/filtered_data_{min}.gexf", "w+") as f:
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




