class Edge:
    def __init__(self, x, y, color, directed):
        """
        Creates a new edge between nodes x and nodes y
        :param x: Node
        :param y: Node
        :param color: RGB code (tuple)
        """
        self.__x = x
        self.__y = y
        self.__color = color
        self.__directed = directed

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, new_x):
        self.__x = new_x

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

    @property
    def directed(self):
        return self.__directed

    @directed.setter
    def directed(self, new_directed):
        self.__directed = new_directed

    def __str__(self):
        return str(self.x.index) + "--->" + str(self.y.index) + " || Color: " + str(self.__color)
