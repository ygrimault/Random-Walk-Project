#!/usr/bin/env python3
import sys
import graph

try:
    import scipy.io as si
except ImportError:
    print("Make sure you installed scipy on your computer")
    si = None
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: ./color file.mat output.mat")
        sys.exit(1)
    mat_file = si.loadmat(sys.argv[1])
    adj_mat = mat_file['A']
    n = len(adj_mat)
    g = graph.Graph(adj_mat)

    output_file = si.loadmat(sys.argv[2])
    colouring = output_file['X'].transpose()[0]
    energy = output_file['E']

    if len(colouring) != n:
        print("Size does not match: %d != %d" % (len(colouring), n))
        sys.exit(1)

    h = 0
    for i in range(g.n):
        for j in g.adjacency[i]:
            if colouring[i] == colouring[j]:
                h += 1

    if int(h / 2) != energy:
        print("The computed energy (%d) is not the energy expected (%d)" % (int(h/2), energy))
        sys.exit(1)

    colours = set()
    for colour in colouring:
        colours.add(colour)

    print("The energy and colouring are consistent.\nUsing %d colours.\nEnergy: %d" % (len(colours), energy))
