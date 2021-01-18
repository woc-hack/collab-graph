import io
import re
import sys
import matplotlib.pyplot as plt
import numpy as np

from frontend.colors import projects_colored, authors_colored

sys.path.append("")

# from frontend.colors import get_color, ProjectsColored
from frontend.data_formatting.graph_structures import Node


def plot_size_distribution(in_path):
    size2count = {}
    min_size = sys.maxsize
    max_size = -sys.maxsize
    nodes_n = 0
    with io.open(in_path) as in_f:
        lines = in_f.readlines()
        n = len(lines)
        for i, line in enumerate(lines):
            node_search = re.search("<node id=\"(\d*)\" label=\"(.*)\" size=\"(.*)\"/>", line, re.IGNORECASE)
            if node_search:
                nodes_n += 1
                node = Node(node_search.group(1), node_search.group(2), float(node_search.group(3)))
                if node.size > max_size:
                    max_size = node.size
                if node.size < min_size:
                    min_size = node.size
                if int(node.size) in size2count:
                    size2count[int(node.size)] += 1
                else:
                    size2count[int(node.size)] = 1

            else:
                nodes_search = re.search("</nodes>", line, re.IGNORECASE)
                if nodes_search:
                    break

        print(min_size, max_size)
        # cut the tail of max keys to see the distribution in detail
        max_keys = sorted(size2count.keys())[-100:]
        filtered_dict = {key: val for key, val in size2count.items() if key not in max_keys}
        plt.bar(list(filtered_dict.keys()), list(filtered_dict.values()), width=10)
        plt.show()


def add_size_and_color(in_path, out_path):
    colored = authors_colored
    with io.open(in_path) as in_f:
        with io.open(out_path, "w+") as out_f:
            lines = in_f.readlines()
            n = len(lines)
            need_to_search = True
            for i, line in enumerate(lines):
                print(i, n)
                if i == 1:
                    out_f.write("<gexf xmlns=\"http://www.gexf.net/1.2draft\" xmlns:viz=\"http://www.gexf.net/1.1draft/viz\">\n")
                    continue
                if i == 2:
                    out_f.write("    <graph mode=\"static\" defaultedgetype=\"undirected\">\n")
                    continue
                if need_to_search:
                    node_search = re.search("<node id=\"(\d*)\" label=\"(.*)\" size=\"(.*)\"/>", line, re.IGNORECASE)
                    if node_search:
                        node = Node(node_search.group(1), node_search.group(2), float(node_search.group(3)))
                        out_f.write(f"           <node id=\"{node.id}\" label=\"{node.label}\">\n")
                        out_f.write(f"              <viz:size value=\"{node.size}\"/>\n")
                        out_f.write(colored.get_color(node.size))
                        out_f.write(f"           </node>\n")
                        continue
                    else:
                        nodes_search = re.search("</nodes>", line, re.IGNORECASE)
                        if nodes_search:
                            need_to_search = False
                out_f.write(line)


if __name__ == "__main__":
    in_path = sys.argv[1]
    out_path = sys.argv[2]
    # plot_size_distribution(in_path)
    add_size_and_color(in_path, out_path)
