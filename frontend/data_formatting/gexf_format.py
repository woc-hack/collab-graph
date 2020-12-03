import io

from frontend.data_formatting.graph_structures import Node, Edge


def start(f):
    f.write("""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://www.gexf.net/1.2draft" version="1.2">
    <graph mode="static" defaultedgetype="directed">""")

def start_nodes(f):
    f.write("       <nodes>\n")


def write_node(f, node: Node):
    f.write(f"           <node id=\"{node.id}\" label=\"{node.label}\" size=\"{node.size}\"/>\n")


def finish_nodes(f):
    f.write("       </nodes>\n")


def start_edges(f):
    f.write("       <edges>\n")


def write_edge(f, edge: Edge):
    f.write(f"           <edge id=\"{edge.id}\" source=\"{edge.source_node_id}\" target=\"{edge.target_node_id}\" "
            f"label=\"{edge.label}\" weight=\"{edge.size}\"/>\n")


def finish_edges(f):
    f.write("       </edges>")


def finish(f):
    f.write("    </graph>\n</gexf>")
