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

    def insert_edge(self, new_edge):
        self.__edges.append(new_edge)

    def remove_edge(self, edge):
        self.__edges.remove(edge)

    def insert_node(self, new_node):
        self.__nodes.append(new_node)

    def remove_node(self, node):
        i = 0
        while len(self.__edges) != 0 and i < len(self.__edges):
            edge = self.__edges[i]
            if edge.x.index == node.index or edge.y.index == node.index:
                self.remove_edge(edge)
                i -= 1
            i += 1
        self.__nodes.remove(node)


