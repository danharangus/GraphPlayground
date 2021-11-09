import pygame
from service.nodeService import NodeService
from domain.node import Node


class UI:
    def __init__(self, node_serv):
        self.__node_service = node_serv
        self.__BLACK = (0, 0, 0)
        self.__WHITE = (255, 255, 255)
        self.__BLUE = (0, 0, 255)

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
        pygame.draw.circle(screen, node.color, (node.x, node.y), 50, width=5)
        node_text = font.render(str(node.index), True, node.color)
        screen.blit(node_text, (node.x - 15, node.y - 35))
        pygame.display.update()

    def draw_nodes(self, screen, font):
        for node in self.__node_service.node_list:
            self.draw_node(node, screen, font)
        self.print_nodes()

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
        while loop:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        loop = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        pos = self.get_pos()
                        new_node = Node(counter, pos[0], pos[1], self.__WHITE)
                        self.__node_service.insert_node(new_node)
                        self.draw_nodes(screen, font)
                        counter += 1
            except Exception as e:
                print(e)
                pygame.quit()
        pygame.quit()


ns = NodeService()
ui = UI(ns)
ui.run()
