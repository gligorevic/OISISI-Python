class Vertex:
    def __init__(self, n):
        self.name = n


class AdjGraph:
    vertices = {}
    edges = []
    edge_indices = {}
    page_ranks = {}

    def add_vertex(self, a):
        if a not in self.vertices.keys():
            vertex = Vertex(a)
            self.vertices[vertex.name] = vertex
            for row in self.edges:
                row.append(0)
            self.edges.append([0] * (len(self.edges) + 1))
            self.edge_indices[vertex.name] = len(self.edge_indices)
            return a
        else:
            return a

    def add_edge(self, u, v, weight=1):
        if u == v:
            return False
        if u in self.vertices and v in self.vertices:
            self.edges[self.edge_indices[u]][self.edge_indices[v]] = weight
            #self.edges[self.edge_indices[v]][self.edge_indices[u]] = weight
            return True
        else:
            return False

    # def print_graph(self):
    #     for v, i in sorted(self.edge_indices.items()):
    #         print(v + ' ', end='')
    #         for j in range(len(self.edges)):
    #             print(self.edges[i][j], end='')
    #         print(' ')

    def vertix_count(self):
        return len(self.vertices)

    def edge_count(self):
        counter = 0
        for i in self.vertices:
            for j in self.vertices:
                if(self.edges[self.edge_indices[j]][self.edge_indices[i]]):
                    counter = counter + 1

        return counter

    def page_rank(self):

        new_ranks = []
        lista_kljuceva = []
        n = 100
        d = 0.85

        for i in self.vertices.keys():
            lista_kljuceva.append(i)
            self.page_ranks[i] = 1 / len(self.vertices.keys())

        while n:
            for v, i in self.edge_indices.items():
                # print(v, i)
                v_rank = 0
                for j in range(len(self.edges)):
                    if self.edges[j][i]:
                        # print("{0} = {1} + {2} / {3}".format(v_rank, v_rank, self.page_ranks[lista_kljuceva[j]], sum(self.edges[j])))
                        if (sum(self.edges[j])):
                            v_rank = v_rank + (self.page_ranks[lista_kljuceva[j]] / sum(self.edges[j]))
                v_rank = (1 - d) + d * v_rank

                new_ranks.append(v_rank)

            for k in range(len(new_ranks)):
                self.page_ranks[lista_kljuceva[k]] = new_ranks[k]
            new_ranks = []
            n = n - 1