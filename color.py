#!/usr/bin/env python3
from math import *
import sys
import numpy
import Graph
import Colouring

try:
    import scipy.io as si
except ImportError:
    print("Make sure you installed scipy on your computer")
    si = None
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: ./color file.mat nb_colors")
        sys.exit(1)
    mat_file = si.loadmat(sys.argv[1])
    adj_mat = mat_file['A']
    g = Graph.Graph(adj_mat)
    nb_colors = int(sys.argv[2])
    coloring = Colouring.Colouring(g, nb_colors, lambda n: 100*0.9**floor(n / 1000))
    h_hist = coloring.metropolis(10000)
    output = {'X': numpy.array([[e] for e in g.coloring]),
              'E': numpy.array(coloring.H)}
    si.savemat('output', output)
    coloring.plot(h_hist)
