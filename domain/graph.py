from copy import deepcopy


class Graph:
    def __init__(self, nodes, edges):
        """
        Creates a new edge between nodes x and nodes y
        :param nodes: Node list
        :param edges: Edge list
        """
        self.__nodes = nodes
        self.__edges = edges

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self, new_nodes):
        self.__nodes = deepcopy(new_nodes)

    @property
    def edges(self):
        return self.__edges

    @edges.setter
    def edges(self, new_edges):
        self.__edges = deepcopy(new_edges)

