class Node:
    def __init__(self, id, label, size, author):
        self.id = id
        self.label = label
        self.size = size
        self.author = author

class Edge:
    def __init__(self, id, source, target, label, size):
        self.id = id
        self.source_node_id = source
        self.target_node_id = target
        self.label = label
        self.size = size
