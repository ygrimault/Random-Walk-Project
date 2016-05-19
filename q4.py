#!/usr/bin/env python3
from math import *
import sys
import Graph
import Colouring

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("Make sure you installed matplotlib on your computer")
    plt = None
    sys.exit(1)

try:
    import scipy.io as si
except ImportError:
    print("Make sure you installed scipy on your computer")
    si = None
    sys.exit(1)

try:
    import progressbar
except ImportError:
    progressbar = None


def plots(hamiltonian_hists):
    """
    :param hamiltonian_hists: list of lists of values to plot with parameters
    """
    for (q_, hamiltonian_hist) in hamiltonian_hists:
        plt.plot(range(len(hamiltonian_hist)), hamiltonian_hist, label="q=%s" % (q_))

    plt.xlabel('Mean connectivity (c)')
    plt.ylabel('Optimal hamiltonian found')
    plt.title('Metropolis Algorithm')
    plt.grid(True)
    plt.legend(frameon=False)
    plt.show()


if __name__ == '__main__':
    qs = [3, 5, 7]
    c_min = 0
    c_max = 30
    n = 1000
    hists = []

    for q in qs:
        hist = []
        r = range(c_min, c_max+1)
        if progressbar:
            r = (progressbar.ProgressBar(redirectouput=True))(r)
        for c in r:
            g = Graph.erdos_renyi(n, c)
            coloring = Colouring.Colouring(g, q, lambda step, b: sqrt(n) * (1 / 0.93) ** floor(step / exp(2 * b)))
            (h_hist, min_index, _) = coloring.metropolis(10 ** 5, get_min=True)
            hist.append(h_hist[min_index])
        hists.append((q, hist))

    plots(hists)
