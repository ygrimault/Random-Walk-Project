#!/usr/bin/env python3
from math import *
import sys
import numpy
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

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: ./color file.mat nb_colors [steps]")
        sys.exit(1)
    mat_file = si.loadmat(sys.argv[1])
    adj_mat = mat_file['A']
    n = len(adj_mat)
    g = graph.Graph(adj_mat)
    nb_colors = int(sys.argv[2])
    coloring = colouring.Colouring(g, nb_colors, lambda step, b: sqrt(n) * (1/0.93) ** floor(step / exp(2*b)))
    nb_steps = 10**4
    if len(sys.argv) >= 4:
        nb_steps = int(sys.argv[3])
    (h_hist, min_index, opt_coloring) = coloring.metropolis(nb_steps, get_min=True)
    print("Minimum energy: %d" % h_hist[min_index])
    print("Reached at: %d" % min_index)
    output = {'X': numpy.array([[e] for e in opt_coloring]),
              'E': numpy.array(h_hist[min_index])}
    si.savemat('output', output)
    plot(h_hist)
