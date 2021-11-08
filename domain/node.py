class Node:
    def __init__(self, index, x, y, color):
        """
        Creates a new Node object
        :param x: x coordinate of the node (float)
        :param y: y coordinate of the node (float)
        :param color: RGB code of the node's color (tuple)
        """
        self.__index = index
        self.__x = x
        self.__y = y
        self.__color = color

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new_x):
        self.__x = new_x

    @property
    def index(self):
        return self.__index

    @index.setter
    def index(self, new_index):
        self.__index = new_index

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, new_y):
        self.__y = new_y

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, new_color):
        self.__color = new_color

    def __str__(self):
        return str(self.__index) +\
               " || Position: " + str(self.x) + ", " + str(self.y)\
               + " || Color: " + str(self.__color)
