
def start(f):
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<gexf xmlns=\"http://www.gexf.net/1.2draft\" version=\"1.2\">\n"
            "    <graph mode=\"static\" defaultedgetype=\"directed\">".decode("utf-8"))

def start_nodes(f):
    f.write("       <nodes>\n".decode("utf-8"))


def write_node(f, node):
    n = "           <node id=\"" + str(node.id) + "\" label=\"" + str(node.label) + "\" size=\"" + str(node.size) + "\"/>\n"
    f.write(n.decode("utf-8"))


def finish_nodes(f):
    f.write("       </nodes>\n".decode("utf-8"))


def start_edges(f):
    f.write("       <edges>\n".decode("utf-8"))


def write_edge(f, id, source, target, size):
    e = "           <edge id=\"" + str(id) + "\" source=\"" + str(source) + "\" target=\"" + str(target) + "\" label=\"" + str(size) + "\" weight=\"" + str(size) + "\"/>\n"
    f.write(e.decode("utf-8"))


def finish_edges(f):
    f.write("       </edges>\n".decode("utf-8"))


def finish(f):
    f.write("    </graph>\n</gexf>".decode("utf-8"))
