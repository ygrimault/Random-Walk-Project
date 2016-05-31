#!/usr/bin/env python3
from math import *
import sys
import numpy
import graph
import colouring
import os
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


def color_thread(thread_number):
    g = graph.Graph(adj_mat)
    coloring = colouring.Colouring(g, nb_colors, lambda step, b: (1/0.93)*b if step % floor(exp(2*b)+0.5) == 0 else b)
    (h_hist_thread, min_index_thread, opt_coloring_thread) = coloring.metropolis(nb_steps, get_min=True, show_progress=True)
    print("Thread %d: Minimum energy: %d" % (thread_number, h_hist_thread[min_index_thread]))
    print("Thread %d: Reached at: %d" % (thread_number, min_index_thread))
    return h_hist_thread, min_index_thread, opt_coloring_thread, thread_number


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: %s input_file.mat nb_colors [steps] [nb_threads]" % sys.argv[0])
        sys.exit(1)
    mat_file = si.loadmat(sys.argv[1])
    adj_mat = mat_file['A']
    n = len(adj_mat)
    nb_colors = int(sys.argv[2])
    nb_steps = 10**4
    if len(sys.argv) >= 4:
        nb_steps = int(sys.argv[3])

    if len(sys.argv) >= 5:
        p = Pool(int(sys.argv[4]))
        results = p.map(color_thread, list(range(int(sys.argv[4]))))
        h_hist, min_index, opt_coloring, thread = min(results, key=lambda e: (e[0])[e[1]])
    else:
        h_hist, min_index, opt_coloring, thread = color_thread(0)

    print("Thread number %d has the best solution." % thread)

    output = {'X': numpy.array([[e] for e in opt_coloring]),
              'E': numpy.array(h_hist[min_index])}
    output_filename = 'output_%s_q%d_E%d' % (os.path.splitext(sys.argv[1])[0], nb_colors, h_hist[min_index])
    si.savemat(output_filename, output)
    # plot(h_hist)
    os.system("./check.py %s %s" % (sys.argv[1], output_filename))
    print()
