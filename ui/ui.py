import pygame
from service.nodeService import NodeService
from service.edgeService import EdgeService
from domain.node import Node
from domain.edge import Edge
from domain.graph import Graph
import math


class UI:
    def __init__(self):
        self.__graph = Graph([], [])
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
        for node in self.__graph.nodes:
            print(node)
        print("**************************")

    def print_edges(self):
        for edge in self.__graph.edges:
            print(edge)
        print("-----------------------------")

    def draw_node(self, node, screen, font):
        rect = pygame.draw.circle(screen, node.color, (node.x, node.y), 40, width=5)
        for n in self.__graph.nodes:
            if n.index == node.index:
                n.rect = rect
        node_text = font.render(str(node.index), True, node.color)
        if node.index < 10:
            screen.blit(node_text, (node.x - 11, node.y - 28))
        elif node.index < 100:
            screen.blit(node_text, (node.x - 22, node.y - 28))
        else:
            screen.blit(node_text, (node.x - 33, node.y - 28))
        pygame.display.update()

    def draw_nodes(self, screen, font):
        for node in self.__graph.nodes:
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
        for edge in self.__graph.edges:
            self.draw_edge(edge, screen, font)
        self.print_edges()

    def draw_graph(self, screen, font, canvas_rect):
        screen.fill(self.__BLACK, canvas_rect)
        self.draw_nodes(screen, font)
        self.draw_edges(screen, font)

    def point_in_rect(self, point, rect):
        x1, y1, w, h = rect
        x2, y2 = x1 + w, y1 + h
        x, y = point
        if x1 <  x < x2:
            if y1 < y < y2:
                return True
        return False

    def validate_edge(self, new_edge):
        for edge in self.__graph.edges:
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

        surface = pygame.Surface((w, h))
        taskbar_rect = pygame.Rect(0, 0, w, 200)
        canvas_rect = pygame.Rect(0, 200, w, h - 200)

        taskbar = surface.subsurface(taskbar_rect)
        canvas = surface.subsurface(canvas_rect)

        taskbar.fill(self.__GREY)
        canvas.fill(self.__BLACK)

        # draw player 1's view  to the top left corner
        screen.blit(taskbar, (0, 0))
        # player 2's view is in the top right corner
        screen.blit(canvas, (0, 200))

        pygame.display.update()

        counter = 0
        loop = True
        source_node = None
        destination_node = None
        while loop:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = self.get_pos()

                        collision = False   # check collision
                        for node in self.__graph.nodes:
                            if node.rect is not None:
                                if self.check_collision(pos, node.rect):
                                    collision = True
                                    break

                        clicked_node = None
                        click = False
                        for node in self.__graph.nodes:
                            if node.rect is not None:
                                if self.point_in_rect(pos, node.rect):
                                    clicked_node = node
                                    click = True
                                    break

                        if event.button == 1:
                            if click:
                                if source_node is None:
                                    source_node = clicked_node
                                else:
                                    if source_node != clicked_node:
                                        new_edge = Edge(source_node, clicked_node, self.__WHITE, False)
                                        self.__graph.insert_edge(new_edge)
                                        self.draw_graph(surface, font, canvas_rect)
                                        screen.blit(surface, (0, 0))
                                        pygame.display.flip()
                                    clicked_node = None
                                    source_node = None
                            elif not collision:
                                if source_node is None:
                                    if pos[1] > 235:
                                        new_node = Node(counter, pos[0], pos[1], self.__WHITE)
                                        self.__graph.insert_node(new_node)
                                        self.draw_graph(surface, font, canvas_rect)
                                        screen.blit(surface, (0, 0))
                                        pygame.display.flip()
                                        counter += 1
                                    else:
                                        source_node = None
                                        clicked_node = None
                                else:
                                    clicked_node = None
                                    source_node = None
                        elif event.button == 3:
                            if click:
                                self.__graph.remove_node(clicked_node)
                                clicked_node = None
                                self.draw_graph(surface, font, canvas_rect)
                                screen.blit(surface, (0, 0))
                                pygame.display.flip()

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
ui = UI()
ui.run()
