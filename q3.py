#!/usr/bin/env python3
from math import *
import sys
import graph
import colouring

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


def plots(hamiltonian_hists):
    """
    :param hamiltonian_hists: list of lists of values to plot with parameters
    """
    for (q_, c_, hamiltonian_hist) in hamiltonian_hists:
        plt.semilogx(range(len(hamiltonian_hist)), hamiltonian_hist, label="q=%s, c=%s" % (q_, c_))

    plt.xlabel('Time (iterations)')
    plt.ylabel('Hamiltonian of the graph')
    plt.title('Metropolis Algorithm')
    plt.grid(True)
    plt.legend(frameon=False)
    plt.show()

if __name__ == '__main__':
    qs = [3, 5, 7]
    cs = [5, 10]

    hists = []
    for q in qs:
        for c in cs:
            n = 1000
            g = graph.erdos_renyi(n, c)
            coloring = colouring.Colouring(g, q, lambda step, b: sqrt(n) * (1/0.93) ** floor(step / exp(2*b)))
            hists.append((q, c, coloring.metropolis(10**6, show_progress=True)))

    for hist in hists:
        print(hist[-1][-1])
    plots(hists)
