from random import *
from math import *

try:
    import progressbar
except ImportError:
    progressbar = None


class Colouring:
    """ All functions related to colouring the graph """

    def __init__(self, graph, q, beta):
        """
        :param graph: Graph to be coloured
        :param q: Total number of colors
        """
        self.graph = graph
        self.q = q
        self.H = None
        self.beta = beta
        self.t = 0
        self.previous_beta = sqrt(self.graph.n)

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
        h = 0
        for i in range(self.graph.n):
            for j in self.graph.adjacency[i]:
                if self.graph.coloring[i] == self.graph.coloring[j]:
                    h += 1
        return int(h/2)

    def metropolis(self, n, show_progress=False, get_min=False):
        self.init_random_coloring()
        hamiltonian_hist = [self.H]
        min_index = 0
        opt_coloring = self.graph.coloring
        if progressbar and show_progress:
            bar = progressbar.ProgressBar(redirectoutput=True)
            r = bar(range(n))
        else:
            r = range(n)
        for _ in r:
            self.step()
            if self.H < hamiltonian_hist[min_index]:
                min_index = len(hamiltonian_hist)
                opt_coloring = self.graph.coloring
            hamiltonian_hist.append(self.H)

        if get_min:
            return hamiltonian_hist, min_index, opt_coloring
        return hamiltonian_hist

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

        self.previous_beta = self.beta(self.t, self.previous_beta)
        if delta <= 0 or random() < exp(-self.previous_beta*delta):
            self.graph.coloring[v] = new_color
            self.H += delta

        self.t += 1
