from domain.node import Node
from copy import deepcopy


class NodeService:
    def __init__(self):
        self.__node_list = []

    @property
    def node_list(self):
        return self.__node_list

    @node_list.setter
    def node_list(self, new_nodes):
        self.__node_list = deepcopy(new_nodes)

    def insert_node(self, new_node):
        self.__node_list.append(new_node)

    def remove_node(self, node):
        self.__node_list.remove(node)
