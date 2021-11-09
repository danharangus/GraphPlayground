import pygame
from service.nodeService import NodeService
from service.edgeService import EdgeService
from domain.node import Node
from domain.edge import Edge
import math


class UI:
    def __init__(self, node_serv, edge_serv):
        self.__node_service = node_serv
        self.__edge_service = edge_serv
        self.__BLACK = (0, 0, 0)
        self.__WHITE = (255, 255, 255)
        self.__BLUE = (0, 0, 255)
        self.__GREY = (134, 140, 150)
        self.__node_rectangles = []

    def get_pos(self):
        """
        Gets the current cursor position
        :return: (x, y) - tuple representing the cursor position
        """
        pos = pygame.mouse.get_pos()
        return pos

    def print_nodes(self):
        for node in self.__node_service.node_list:
            print(node)
        print("**************************")

    def print_edges(self):
        for edge in self.__edge_service.edge_list:
            print(edge)
        print("-----------------------------")

    def draw_node(self, node, screen, font):
        rect = pygame.draw.circle(screen, node.color, (node.x, node.y), 40, width=5)
        self.__node_rectangles.append((node.index, rect))
        node_text = font.render(str(node.index), True, node.color)
        if node.index < 10:
            screen.blit(node_text, (node.x - 11, node.y - 28))
        elif node.index < 100:
            screen.blit(node_text, (node.x - 22, node.y - 28))
        else:
            screen.blit(node_text, (node.x - 33, node.y - 28))
        pygame.display.update()

    def draw_nodes(self, screen, font):
        self.__node_rectangles.clear()
        if len(self.__node_service.node_list) == 0:
            screen.fill(self.__BLACK)
        for node in self.__node_service.node_list:
            self.draw_node(node, screen, font)
        self.print_nodes()

    def check_collision(self, point, rect):
        x1, y1, w, h = rect
        x2, y2 = x1 + w + 30, y1 + h + 30
        x1 -= 30
        y1 -= 30
        x, y = point
        if x1 < x < x2:
            if y1 < y < y2:
                return True
        return False

    def draw_edge(self, edge, screen, font):
        n1 = edge.x
        n2 = edge.y
        vx = (n1.x - n2.x)
        vy = (n1.y - n2.y)
        ux = vx / (math.sqrt(vx * vx + vy * vy))
        uy = vy / (math.sqrt(vx * vx + vy * vy))
        xf1 = float(n1.x - 40 * ux)
        xf2 = float(n2.x + 40 * ux)
        yf1 = float(n1.y - 40 * uy)
        yf2 = float(n2.y + 40 * uy)
        color = edge.color
        pygame.draw.line(screen, color,
                         (xf1, yf1),
                         (xf2, yf2), 2)
        pygame.display.update()

    def draw_edges(self, screen, font):
        for edge in self.__edge_service.edge_list:
            self.draw_edge(edge, screen, font)
        self.print_edges()

    def point_in_rect(self, point, rect):
        x1, y1, w, h = rect
        x2, y2 = x1 + w, y1 + h
        x, y = point
        if x1 <  x < x2:
            if y1 < y < y2:
                return True
        return False

    def validate_edge(self, new_edge):
        for edge in self.__edge_service.edge_list:
            if new_edge.x == edge.x and new_edge.y == edge.y:
                return False
        return True

    def run(self):
        pygame.init()
        pygame.font.init()
        font = pygame.font.SysFont('Arial', 45)

        w = 1920
        h = 1080
        screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Graph Playground")
        screen.fill(self.__BLACK)
        taskbar = pygame.Rect(0, 0, w, 150)
        sub1 = screen.subsurface(taskbar)
        sub1.fill(self.__GREY)
        pygame.display.update()
        loop = True

        counter = 0
        source_node = None
        selected_rect = None
        offset_x = 0
        offset_y = 0
        dest_node = None
        while loop:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = self.get_pos()
                        if pos[1] > 180:
                            click_on_node = False
                            clicked_node = -1
                            collision = False
                            for node_rect in self.__node_rectangles:
                                rect = node_rect[1]
                                if self.point_in_rect(pos, rect):
                                    print("Click on node", node_rect[0])
                                    click_on_node = True
                                    clicked_node = node_rect[0]

                                if self.check_collision(pos, rect):
                                    collision = True

                            if event.button == 1:
                                if not click_on_node:
                                    if not collision:
                                        new_node = Node(counter, pos[0], pos[1], self.__WHITE)
                                        self.__node_service.insert_node(new_node)
                                        self.draw_nodes(screen, font)
                                        counter += 1
                                        source_node = None
                                        dest_node = None
                                else:
                                    if source_node is None:
                                        for node in self.__node_service.node_list:
                                            if node.index == clicked_node:
                                                source_node = node
                                    else:
                                        for node in self.__node_service.node_list:
                                            if node.index == clicked_node:
                                                dest_node = node

                                        if source_node != dest_node:
                                            new_edge = Edge(source_node, dest_node, self.__WHITE, False)
                                            if self.validate_edge(new_edge):
                                                self.__edge_service.insert_edge(new_edge)
                                                self.draw_edges(screen, font)

                                        source_node = None
                                        dest_node = None
                            elif event.button == 3:
                                if click_on_node:
                                    if source_node is None:
                                        for node in self.__node_service.node_list:
                                            if node.index == clicked_node:
                                                source_node = node
                                    self.__node_service.remove_node(source_node)
                                    print(self.__node_service.node_list)
                                    screen.fill(self.__BLACK)
                                    self.draw_nodes(screen, font)
                                    source_node = None
                                    print("removed")
                    elif event.type == pygame.MOUSEBUTTONUP:
                        pass
                    elif event.type == pygame.MOUSEMOTION:
                        pass
            except Exception as e:
                print(e)
                pygame.quit()
        pygame.quit()


ns = NodeService()
es = EdgeService()
ui = UI(ns, es)
ui.run()
