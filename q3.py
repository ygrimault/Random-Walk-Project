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
    qs = [3, 5, 7]
    cs = [5, 10]

    hists = []
    for q in qs:
        for c in cs:
            n = 1000
            g = Graph.erdos_renyi(n, c)
            coloring = Colouring.Colouring(g, q, lambda step, b: sqrt(n) * (1/0.93) ** floor(step / exp(2*b)))
            hists.append((q, c, coloring.metropolis(16000)))

    Colouring.Colouring.plots(hists)
