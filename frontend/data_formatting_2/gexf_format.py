
def start(f):
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<gexf xmlns=\"http://www.gexf.net/1.2draft\" version=\"1.2\">\n"
            "    <graph mode=\"static\" defaultedgetype=\"directed\">".decode("utf-8"))

def start_nodes(f):
    f.write("       <nodes>\n".decode("utf-8"))


def write_node(f, node):
    n = "           <node id=\"" + str(node.id) + "\" label=\"" + str(node.label) + "\"/>\n"
    f.write(n.decode("utf-8"))


def finish_nodes(f):
    f.write("       </nodes>\n".decode("utf-8"))


def start_edges(f):
    f.write("       <edges>\n".decode("utf-8"))


def write_edge(f, edge):
    e = "           <edge id=\"" + str(edge.id) + "\" source=\"" + str(edge.source_node_id) + "\" target=\"" + str(edge.target_node_id) + "\" label=\"" + str(edge.size) + "\" weight=\"" + str(edge.size) + "\"/>\n"
    f.write(e.decode("utf-8"))


def finish_edges(f):
    f.write("       </edges>\n".decode("utf-8"))


def finish(f):
    f.write("    </graph>\n</gexf>".decode("utf-8"))
