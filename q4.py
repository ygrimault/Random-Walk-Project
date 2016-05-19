#!/usr/bin/env python3
from math import *
import sys
import graph
import colouring
from multiprocessing import Pool

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
    import numpy
except ImportError:
    print("Make sure you installed numpy on your computer")
    numpy = None
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
        plt.plot(numpy.linspace(c_min, c_max, nb_points), hamiltonian_hist, label="q=%s" % q_)

    plt.xlabel('Density (c)')
    plt.ylabel('Optimal hamiltonian found')
    plt.grid(True)
    plt.legend(frameon=False)
    plt.show()


def one_curve(q):
    hist = []
    r = numpy.linspace(c_min, c_max, nb_points)
    if progressbar:
        r = (progressbar.ProgressBar(redirect_stdout=True))(r)
    for c in r:
        g = graph.erdos_renyi(n, c)
        coloring = colouring.Colouring(g, q, lambda step, b: (1/0.93)*b if step % floor(exp(2*b)+0.5) == 0 else b)
        (h_hist, min_index, _) = coloring.metropolis(10 ** 5, get_min=True)
        hist.append(h_hist[min_index])
    return q, hist

if __name__ == '__main__':
    qs = [3, 5, 7]
    c_min = 0
    c_max = 50
    nb_points = 100
    n = 1000
    p = Pool(3)
    hists = p.map(one_curve, qs)

    plots(hists)
