from random import *
from math import *


class Colouring:
    """ All functions related to colouring the graph """

    def __init__(self, graph, q, beta):
        """
        :param graph: Graph to be coloured
        :param q: Total number of colors
        """
        self.graph = graph
        self.q = q
        self.beta = beta
        self.t = 0

    def init_random_coloring(self):
        """
        Assign a random coloring to the graph.
        """
        self.graph.coloring = [randrange(self.q) for _ in range(self.graph.n)]
        self.H = self.hamiltonian()

    def hamiltonian(self):
        """
        :return: The Hamiltonian function of the current coloring (we suppose that every vertex has been colored
        """
        return \
            sum(map(
                    lambda a:
                    sum(filter(
                            lambda b: int(self.graph.coloring[a] == self.graph.coloring[b]),
                            self.graph.adjacency[a])),
                    range(self.graph.n)))\
            / 2

    def metropolis(self, n):
        self.init_random_coloring()
        H_hist = [self.H]
        for _ in range(n):
            self.step()
            H_hist.append(self.H)

        return H_hist

    def step(self):
        v = randrange(self.graph.n)
        old_color = self.graph.coloring[v]
        new_color = randrange(self.q-1)
        if new_color >= old_color:
            new_color += 1
        delta = 0
        for u in self.graph.adjacency[v]:
            if self.graph.coloring[u] == new_color:
                delta += 1
            elif self.graph.coloring[u] == old_color:
                delta -= 1

        if delta <= 0 or random() < exp(-self.beta(self.t)*delta):
            self.graph.coloring[v] = new_color
            self.H += delta

        self.t += 1
