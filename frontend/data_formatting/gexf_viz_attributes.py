import io
import re

from frontend.colors import get_color
from frontend.data_formatting.graph_structures import Node

with io.open("../data/filtered_edges_60_authors_50.gexf") as in_f:
    with io.open("../data/filtered_edges_60_authors_50.gexf", "w+") as out_f:
        lines = in_f.readlines()
        n = len(lines)
        need_to_search = True
        for i, line in enumerate(lines):
            print(i, n)
            if need_to_search:
                node_search = re.search("<node id=\"(\d*)\" label=\"(.*)\" size=\"(.*)\"/>", line, re.IGNORECASE)
                if node_search:
                    node = Node(node_search.group(1), node_search.group(2), float(node_search.group(3)))
                    out_f.write(f"           <node id=\"{node.id}\" label=\"{node.label}\">\n")
                    out_f.write(f"              <viz:size value=\"{node.size}\"/>\n")
                    out_f.write(get_color(node.size))
                    out_f.write(f"           </node>\n")
                    continue
                else:
                    nodes_search = re.search("</nodes>", line, re.IGNORECASE)
                    if nodes_search:
                        need_to_search = False
            out_f.write(line)
