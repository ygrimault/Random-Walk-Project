class Graph:
    """ Graph with vertices that can be colored """

    def __init__(self, vertices=None, edges=None):
        """
        :param vertices: List of vertices
        :param edges: List of edges
        """
        if vertices == None:
            self.vertices = []
        else:
            self.vertices = vertices

        if edges == None:
            self.edges = []
        else:
            self.edges = edges

    def add_edge(self, edges):
        """
        :param edges: List of edges to be added (tuple of 2 vertices)
        """
        for edge in edges:
            self.edges.append(edge)

    def neighbours(self, vertice):
        """
        :param vertice: A vertex to be studied for neighbours
        :return: List of vertices that share an edge with vertice
        """
        neighbours = []
        for (a,b) in self.edges:
            if a == vertice:
                neighbours.append(b)
            elif b == vertice:
                neighbours.append(a)
        return neighbours

    def __repr__(self):
        string = "List of vertices :\n"
        for vertex in self.vertices:
            strv = repr(vertex)
            string += "  " + strv + "\n"
        string += "\n" + "List of edges :\n"
        for (a,b) in self.edges:
            stra = repr(a)
            strb = repr(b)
            string += "  " + stra + " <--> " + strb + "\n"
        string += "\n"
        return string