import re
import io

from frontend.data_formatting.gexf_format import start, start_nodes, write_node, finish_nodes, start_edges, write_edge, \
    finish_edges, finish
from frontend.data_formatting.graph_structures import Node, Edge

# node id to node
id2n = {}
nodes_ids = set()
nodes = []
edges = []

nodes_min = 50
edges_min = 70

before_filtering_edges = 0
after_filtering_edges = 0

max_nodes_size = 0


with io.open("../data/filtered_authors_50.gexf") as f:
    for line in f:
        node_search = re.search("<node id=\"(\d*)\" label=\"(.*)\" size=\"(.*)\"/>", line, re.IGNORECASE)
        if node_search:
            node = Node(node_search.group(1), node_search.group(2), float(node_search.group(3)))
            # filter out all nodes that don't meet the size requirements
            if node.size >= nodes_min:
                if node.size > max_nodes_size:
                    max_nodes_size = node.size
                id2n[node.id] = node

        edge_search = re.search("<edge id=\"(\d*)\" source=\"(\d*)\" target=\"(\d*)\" label=\"(.*)\" weight=\"(.*)\"/>",
                                line, re.IGNORECASE)
        # by the time we process an edge all nodes should be already processed
        if edge_search:
            before_filtering_edges += 1
            edge = Edge(edge_search.group(1), edge_search.group(2), edge_search.group(3), edge_search.group(4), float(edge_search.group(5)))
            if edge.size >= edges_min and edge.source_node_id in id2n and edge.target_node_id in id2n:
                if edge.source_node_id not in nodes_ids:
                    nodes_ids.add(edge.source_node_id)
                    nodes.append(id2n[edge.source_node_id])
                if edge.target_node_id not in nodes_ids:
                    nodes_ids.add(edge.target_node_id)
                    nodes.append(id2n[edge.target_node_id])
                after_filtering_edges += 1
                edges.append(edge)


print(len(nodes))
print(len(edges))
print(before_filtering_edges, after_filtering_edges)
print(f"max nodes size: {max_nodes_size}")

with io.open(f"../data/filtered_edges_{edges_min}_authors_50.gexf", "w+") as f:
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




