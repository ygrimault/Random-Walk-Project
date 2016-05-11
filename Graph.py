from random import *

class Graph:
    """ Graph with vertices that can be colored """

    def __init__(self, n, mat):
        self.n = n
        self.adjacency = list(map(lambda row: set([i for i, x in enumerate(row) if x == 1]), mat))
        self.coloring = [0 for _ in range(n)]

    def __repr__(self):
        string = "List of vertices :\n"
        for vertex in range(self.n):
            strv = repr(vertex)
            string += "  " + strv + "\n"
        string += "\n" + "List of edges :\n"
        for a in range(self.n):
            for b in self.adjacency[a]:
                stra = repr(a)
                strb = repr(b)
                string += "  " + stra + " <--> " + strb + "\n"
        string += "\n"
        return string


def erdos_renyi(n, c):
    mat = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i):
            r = int(random() < 1.0 * c / n)
            mat[i][j] = r
            mat[j][i] = r
    return Graph(n, mat)
