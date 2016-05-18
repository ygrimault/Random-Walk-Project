#!/usr/bin/env python3
from math import *
import sys
import Graph
import Colouring

try:
    import scipy.io as si
except ImportError:
    print("Make sure you installed scipy on your computer")
    si = None
    sys.exit(1)

if __name__ == '__main__':
    qs = [3, 7]
    cs = [2, 10]

    hists = []
    for q in qs:
        for c in cs:
            g = Graph.erdos_renyi(1000, c)
            coloring = Colouring.Colouring(g, q, lambda n: 500*0.99 ** floor(n / 50))
            hists.append((q, c, coloring.metropolis(1000)))

    Colouring.Colouring.plots(hists)
