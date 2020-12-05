from dataclasses import dataclass

@dataclass
class Project:
    index: int

@dataclass
class Author:
    index: int

@dataclass
class Node:
    id: str
    label: str
    size: float


@dataclass
class Edge:
    id: str
    source_node_id: str
    target_node_id: str
    label: str
    size: float
