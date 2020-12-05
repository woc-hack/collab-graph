import io
import re

from frontend.data_formatting.gexf_format import write_edge
from frontend.data_formatting.graph_structures import Node, Edge

with io.open("../data/filtered_projects_50.gexf") as in_f:
    with io.open("../data/filtered_edges_5_projects_50.gexf", "w+") as out_f:
        lines = in_f.readlines()
        n = len(lines)
        before_filtering = 0
        after_filtering = 0
        for i, line in enumerate(lines):
            print(i, n)
            edge_search = re.search(
                "<edge id=\"(\d*)\" source=\"(\d*)\" target=\"(\d*)\" label=\"(.*)\" weight=\"(.*)\"/>",
                line, re.IGNORECASE)
            if edge_search:
                before_filtering += 1
                edge = Edge(edge_search.group(1), edge_search.group(2), edge_search.group(3), edge_search.group(4),
                            float(edge_search.group(5)))
                if edge.size >= 5:
                    after_filtering += 1
                    write_edge(out_f, edge)
            else:
                out_f.write(line)

print(before_filtering, after_filtering)