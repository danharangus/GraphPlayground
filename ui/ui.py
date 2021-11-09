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

    def draw_node(self, node, screen, font):
        rect = pygame.draw.circle(screen, node.color, (node.x, node.y), 50, width=5)
        self.__node_rectangles.append((node.index, rect))
        node_text = font.render(str(node.index), True, node.color)
        screen.blit(node_text, (node.x - 15, node.y - 35))
        pygame.display.update()

    def check_collision(self, point, rect):
        x1, y1, w, h = rect
        x2, y2 = x1 + w + 35, y1 + h + 35
        x1 -= 35
        y1 -= 35
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
        xf1 = float(n1.x - 46 * ux)
        xf2 = float(n2.x + 46 * ux)
        yf1 = float(n1.y - 46 * uy)
        yf2 = float(n2.y + 46 * uy)
        color = edge.color
        pygame.draw.line(screen, color,
                         (xf1, yf1),
                         (xf2, yf2), 2)
        pygame.display.update()

    def draw_nodes(self, screen, font):
        for node in self.__node_service.node_list:
            self.draw_node(node, screen, font)
        self.print_nodes()

    def draw_edges(self, screen, font):
        for edge in self.__edge_service.edge_list:
            self.draw_edge(edge, screen, font)

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
        font = pygame.font.SysFont('Arial', 60)

        screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Graph Playground")
        screen.fill(self.__BLACK)
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
                        click_on_node = False
                        clicked_node = -1
                        collision = False
                        for node_rect in self.__node_rectangles:
                            rect = node_rect[1]
                            if self.point_in_rect(pos, rect):
                                print("Click on node", node_rect[0])
                                click_on_node = True
                                clicked_node = node_rect[0]
                                selected_rect = node_rect[1]
                                offset_x = selected_rect.x - pos[0]
                                offset_y = selected_rect.y - pos[1]

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
                    elif event.type == pygame.MOUSEBUTTONUP:
                        selected_rect = None
                    elif event.type == pygame.MOUSEMOTION:
                        if selected_rect is not None and source_node is not None:
                            mouse_x, mouse_y = event.pos
                            selected_rect.x = mouse_x + offset_x
                            selected_rect.y = mouse_y + offset_y
                            source_node.x = selected_rect.x
                            source_node.y = selected_rect.y
                            screen.fill(self.__BLACK)
                            self.draw_nodes(screen, font)
                            self.draw_edges(screen, font)
                            pygame.display.flip()
            except Exception as e:
                print(e)
                pygame.quit()
        pygame.quit()


ns = NodeService()
es = EdgeService()
ui = UI(ns, es)
ui.run()
