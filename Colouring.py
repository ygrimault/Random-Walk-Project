class Colouring:
    """ All functions related to colouring the graph """

    def __init__(self, graph, q):
        """
        :param graph: Graph to be coloured
        :param q: Total number of colors
        """
        self.vertices = graph.vertices
        self.edges = graph.edges
        self.colors = range(q)

    def coloring(self, coloring):
        """
        :param coloring: List of tuples (vertex,color)
        """
        for (vertex,color) in coloring:
            vertex.color = color

    def hamiltonian(self):
        """
        :return: The Hamiltonian function of the current coloring (we suppose that every vertex has been colored
        """
        h = 0
        for (a,b) in self.edges:
            if a.color == b.color:
                h += 1
        return h

