class KruskalGraph:

    def __init__(self, vertices):
        self.V = vertices
        self.graph = []

    def add_edge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])

    def union(self, parent, rank, x, y):
        rx = self.find(parent, x)
        ry = self.find(parent, y)

        if rank[rx] < rank[ry]:
            parent[rx] = ry
        elif rank[rx] > rank[ry]:
            parent[ry] = rx
        else:
            parent[ry] = rx
            rank[rx] += 1

    def get_mst(self):
        result = []
        self.graph = sorted(self.graph, key=lambda item: item[2])

        parent = []
        rank = []

        for node in range(self.V):
            parent.append(node)
            rank.append(0)

        n = i = 0
        while n < self.V - 1:

            u, v, w = self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)

            if x != y:
                n = n + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
            # Else discard the edge

        cost = 0
        for u, v, weight in result:
            cost += weight
            print("%d -- %d == %d" % (u, v, weight))
        print("Minimum Spanning Tree cost:", cost)
        return result

