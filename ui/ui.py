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
        self.__BUTTON_SELECTED = (170, 170, 170)
        self.__BUTTON_NORMAL = (0, 102, 204)
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
            screen.blit(node_text, (node.x - 8, node.y - 20))
        elif node.index < 100:
            screen.blit(node_text, (node.x - 14, node.y - 20))
        else:
            screen.blit(node_text, (node.x - 20, node.y - 20))
        pygame.display.update()

    def draw_nodes(self, screen, font):
        for node in self.__graph.nodes:
            self.draw_node(node, screen, font)
        self.print_nodes()

    def check_node_collision(self, point, rect):
        x1, y1, w, h = rect
        x2, y2 = x1 + w + 30, y1 + h + 30
        x1 -= 30
        y1 -= 30
        x, y = point
        if x1 < x < x2:
            if y1 < y < y2:
                return True
        return False

    def draw_arrow(self, node1, node2, screen, color):
        vx = float(node2.x - node1.x)
        vy = float(node2.y - node1.y)

        ux = vx / (math.sqrt(vx * vx + vy * vy))

        uy = vy / (math.sqrt(vx * vx + vy * vy))
        xf1 = float(node1.x + 40 * ux)
        xf2 = float(node2.x - 40 * ux)
        yf1 = float(node1.y + 40 * uy)
        yf2 = float(node2.y - 40 * uy)

        theta = math.pi / 6

        rvx1 = float(-vx * math.cos(theta) + vy * math.sin(theta))

        rvy1 = float(-vx * math.sin(theta) - vy * math.cos(theta))

        rv1len = math.sqrt(rvx1 * rvx1 + rvy1 * rvy1)

        rvx2 = float(-vx * math.cos(-theta) + vy * math.sin(-theta))
        rvy2 = float(-vx * math.sin(-theta) - vy * math.cos(-theta))

        rv2len = math.sqrt(rvx2 * rvx2 + rvy2 * rvy2)

        p1x = float(xf2 + rvx1 / rv1len * 40)
        p1y = float(yf2 + rvy1 / rv1len * 40)
        p2x = float(xf2 + rvx2 / rv2len * 40)
        p2y = float(yf2 + rvy2 / rv2len * 40)
        pygame.draw.line(screen, color, (xf2, yf2), (p1x, p1y))
        pygame.draw.line(screen, color, (xf2, yf2), (p2x, p2y))


    def draw_edge(self, edge, screen):
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
        rect = pygame.draw.line(screen, color,
                         (xf1, yf1),
                         (xf2, yf2), 2)
        if edge.directed is True:
            self.draw_arrow(edge.x, edge.y, screen, color)
        for e in self.__graph.edges:
            if e.x == edge.x and e.y == edge.y:
                e.rect = rect
                break
        pygame.display.update()

    def draw_edges(self, screen):
        for edge in self.__graph.edges:
            self.draw_edge(edge, screen)
        self.print_edges()

    def draw_graph(self, screen, font, canvas_rect):
        screen.fill(self.__BLACK, canvas_rect)
        self.draw_nodes(screen, font)
        self.draw_edges(screen)

    def point_in_rect(self, point, rect):
        x1, y1, w, h = rect
        x2, y2 = x1 + w, y1 + h
        x, y = point
        if x1 < x < x2:
            if y1 < y < y2:
                return True
        return False

    def check_edge_click(self, point, rect):
        x1, y1, w, h = rect
        x2, y2 = x1 + w, y1 + h
        x, y = point
        if x1 < x < x2:
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
        font = pygame.font.SysFont('Arial', 30)
        w = 1280
        h = 780
        screen = pygame.display.set_mode((w, h))

        surface = pygame.Surface((w, h))
        taskbar_rect = pygame.Rect(0, 0, w, 200)
        canvas_rect = pygame.Rect(0, 200, w, h - 200)

        taskbar = surface.subsurface(taskbar_rect)
        canvas = surface.subsurface(canvas_rect)

        taskbar.fill(self.__GREY)
        canvas.fill(self.__BLACK)

        # draw taskbar
        screen.blit(taskbar, (0, 0))
        # draw canvas
        screen.blit(canvas, (0, 200))

        directed_button_message = "Directed"
        is_directed = False
        directed_button_position_text_w_ratio = 17
        directed_button_position_text_h_ratio = 18
        directed_button_position_w_ratio = 9
        directed_button_position_h_ratio = 18
        directed_button_text_w_offset = 17
        button_text = font.render(directed_button_message, True, self.__WHITE)
        directed_button = pygame.Rect(w / directed_button_position_text_w_ratio,
                                      h / directed_button_position_text_h_ratio,
                                      w / directed_button_position_w_ratio,
                                      h / directed_button_position_h_ratio)
        pygame.draw.rect(screen, self.__BUTTON_NORMAL, directed_button)
        screen.blit(button_text, (w / directed_button_position_text_w_ratio + directed_button_text_w_offset,
                                  h / directed_button_position_text_h_ratio))
        pygame.display.update()

        counter = 0
        loop = True
        source_node = None
        destination_node = None
        while loop:
            pygame.draw.rect(screen, self.__BUTTON_NORMAL, directed_button)
            screen.blit(button_text, (w / directed_button_position_text_w_ratio + directed_button_text_w_offset,
                                      h / directed_button_position_text_h_ratio))
            pygame.display.flip()
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        pos = self.get_pos()

                        node_collision = False   # check collision
                        for node in self.__graph.nodes:
                            if node.rect is not None:
                                if self.check_node_collision(pos, node.rect):
                                    node_collision = True
                                    break

                        clicked_node = None
                        clicked_edge = None
                        node_click = False
                        edge_click = False

                        for node in self.__graph.nodes:
                            if node.rect is not None:
                                if self.point_in_rect(pos, node.rect):
                                    clicked_node = node
                                    node_click = True
                                    break

                        if not node_click:
                            for edge in self.__graph.edges:
                                if edge.rect is not None:
                                    if self.check_edge_click(pos, edge.rect):
                                        edge_click = True
                                        clicked_edge = edge
                                        break

                        if event.button == 1:
                            if w/17 <= float(pos[0]) <= w / directed_button_position_text_w_ratio + w / 10 and \
                                    h / directed_button_position_text_h_ratio <= float(pos[1]) <= h / directed_button_position_text_h_ratio + h / 20:
                                # Click on directed/undirected button
                                if directed_button_message == "Directed":
                                    directed_button_message = "Undirected"
                                    is_directed = True
                                    for edge in self.__graph.edges:
                                        edge.directed = True
                                else:
                                    directed_button_message = "Directed"
                                    is_directed = False
                                    for edge in self.__graph.edges:
                                        edge.directed = False
                                self.draw_graph(surface, font, canvas_rect)
                                screen.blit(surface, (0, 0))

                                button_text = font.render(directed_button_message, True, self.__WHITE)
                                directed_button = pygame.Rect(w / directed_button_position_text_w_ratio,
                                                              h / directed_button_position_text_h_ratio, w / 9, h / 20)
                                pygame.draw.rect(screen, self.__BUTTON_NORMAL, directed_button)
                                screen.blit(button_text, (w / directed_button_position_text_w_ratio + directed_button_text_w_offset,
                                                          h / directed_button_position_text_h_ratio))
                                pygame.display.update()
                                continue
                            if node_click:
                                if source_node is None:
                                    source_node = clicked_node
                                    source_node.color = self.__BLUE
                                    self.draw_graph(surface, font, canvas_rect)
                                    screen.blit(surface, (0, 0))
                                    pygame.display.flip()
                                else:
                                    if source_node != clicked_node:
                                        new_edge = Edge(source_node, clicked_node, self.__WHITE, is_directed)
                                        self.__graph.insert_edge(new_edge)
                                        self.draw_graph(surface, font, canvas_rect)
                                        screen.blit(surface, (0, 0))
                                        pygame.display.flip()
                                    source_node.color = self.__WHITE
                                    self.draw_graph(surface, font, canvas_rect)
                                    screen.blit(surface, (0, 0))
                                    pygame.display.flip()
                                    clicked_node = None
                                    source_node = None
                            elif not node_collision:
                                if source_node is None:
                                    if pos[1] > 235:
                                        # Add new node
                                        new_node = Node(counter, pos[0], pos[1], self.__WHITE)
                                        self.__graph.insert_node(new_node)
                                        self.draw_graph(surface, font, canvas_rect)
                                        screen.blit(surface, (0, 0))
                                        pygame.display.flip()
                                        counter += 1
                                else:
                                    source_node.color = self.__WHITE
                                    self.draw_graph(surface, font, canvas_rect)
                                    screen.blit(surface, (0, 0))
                                    pygame.display.flip()
                                    clicked_node = None
                                    source_node = None
                        elif event.button == 3:
                            if node_click:
                                # Remove node
                                self.__graph.remove_node(clicked_node)
                                clicked_node = None
                                self.draw_graph(surface, font, canvas_rect)
                                screen.blit(surface, (0, 0))
                                pygame.display.flip()
                            elif edge_click:
                                self.__graph.remove_edge(clicked_edge)
                                clicked_edge = None
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
