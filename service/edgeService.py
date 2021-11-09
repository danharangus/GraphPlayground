from domain.node import Node
from copy import deepcopy


class EdgeService:
    def __init__(self):
        self.__edge_list = []

    @property
    def edge_list(self):
        return self.__edge_list

    @edge_list.setter
    def edge_list(self, new_edges):
        self.__edge_list = deepcopy(new_edges)

    def insert_edge(self, new_edge):
        self.__edge_list.append(new_edge)
