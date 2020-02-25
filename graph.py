class Graph:
    class Edge:

        class Vertex:
            __slots__ = '_element'

            def __init__(self, x):
                self._element = x

            def element(self):
                return self._element()

            def __hash__(self):
                return hash(id(self))

            def __str__(self):
                return str(self._element)

        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, u, v, x):
            self._origin = u
            self._destination = v
            self._element = x

        def endpoints(self):
            return self._origin, self._destination

        def opposite(self, v):
            if not isinstance(v, self.Vertex):
                raise TypeError('v must be Vertex')
            return self._destination if v is self._origin else self._origin
        # raise ValueError('v not incident to edge')

        def element(self):
            return self._element

        def __hash__(self):
            return hash((self._origin, self._destination))

        def __str__(self):
            return '({0},{1},{2})'.format(self._origin, self._destination, self._element)

    def __init__(self, directed=False):
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing
        self._vertices = {}

    def _validate_vertex(self, v):
        if not isinstance(v, self.Edge.Vertex):
            raise TypeError('vertex exppected')
        if v not in self._outgoing:
            raise ValueError('vertex does not belong to this graph')

    def is_directed(self):
        return self._incoming is not self._outgoing

    def vertex_count(self):
        return len(self._outgoing)

    def vertices(self):
        return self._outgoing.keys()

    def edge_count(self):
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        return total if self.is_directed() else total // 2

    def edges(self):
        result = set()
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        if self._vertices.get(x):
            return self._vertices[x]
        else:
            v = self.Edge.Vertex(x)
            self._vertices[x] = v
            self._outgoing[v] = {}
            if self.is_directed():
                self._incoming[v] = {}
            return v


    def insert_edge(self, u, v, x=None):
        if self.get_edge(u, v) is not None:
            raise ValueError('u and v are already adjacent')
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[u][v] = e
