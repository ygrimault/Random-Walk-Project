from random import *
from math import *
import sys

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Make sure you installed matplotlib on your computer")
    plt = None
    sys.exit(1)


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
        hamiltonian_hist = [self.H]
        for _ in range(n):
            self.step()
            hamiltonian_hist.append(self.H)

        return hamiltonian_hist

    @staticmethod
    def plot(hamiltonian_hist):
        """
        :param hamiltonian_hist: list of values to plot
        """
        plt.plot(hamiltonian_hist)
        plt.xlabel('Time (iterations)')
        plt.ylabel('Hamiltonian of the graph')
        plt.title('Metropolis Algorithm')
        plt.grid(True)
        plt.show()

    @staticmethod
    def plots(hamiltonian_hists):
        """
        :param hamiltonian_hists: list of lists of values to plot with parameters
        """
        for (q, c, hamiltonian_hist) in hamiltonian_hists:
            plt.plot(range(len(hamiltonian_hist)), hamiltonian_hist, label="q=%s, c=%s" % (q, c))

        plt.xlabel('Time (iterations)')
        plt.ylabel('Hamiltonian of the graph')
        plt.title('Metropolis Algorithm')
        plt.grid(True)
        plt.legend(frameon=False)
        plt.show()

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
