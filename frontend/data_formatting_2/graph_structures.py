class Node:
    def __init__(self, id, label, size, project):
        self.id = id
        self.label = label
        self.size = size
        self.project = project

class Edge:
    def __init__(self, id, source, target, label, size):
        self.id = id
        self.source_node_id = source
        self.target_node_id = target
        self.label = label
        self.size = size
