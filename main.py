import Graph
import Bandit
import sys

try:
    import scipy.io as si
except ImportError:
    print("Make sure you installed scipy on your computer")
    si = None
    sys.exit(1)


def beta(t):
    return 1.0/(t**.5+1)

if __name__ == '__main__':
    # Import the mat file that is in the same directory
    file_name = 'graph_adjacency_matrix'
    mat_file = si.loadmat(file_name)
    adj_mat = mat_file['A']
    # Now we can create a graph using this array (I tested the function)
    # Create a random graph with N = 1000 vertices
    g = Graph.erdos_renyi(1000, 1.87)
    # Create a colouring with q = 750 and a beta function
    # c = Colouring.Colouring(g, 550, beta)
    # # number of iterations
    # iter_num = int(2e5)
    # # plot the results using the poor-man's plot
    # CMDPlot.command_line_plot(c.metropolis(iter_num), x_precision=120, y_precision=60)

    bandit = Bandit.BanditBeta(g, 350, metropolis_iter=1e4)
    bandit.train(1000)
