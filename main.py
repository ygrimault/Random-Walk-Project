import graph
import bandit
import sys
from math import exp, floor, log
from random import random

try:
    import scipy.io as si
except ImportError:
    print("Make sure you installed scipy on your computer")
    si = None
    sys.exit(1)

def exp_template(T0, a, tau):
    def _exp_template(x, y):
        try:
            return abs(T0+1e-5) * exp(abs(a+1e-5)*floor(x/abs(tau+1e-5)))
        except:
            return 1e10
    return _exp_template

def log_template(D, a, t):
    def _log_template(x, y):
        return abs((D+1e-5)*log((a+1e-5)*floor(x/(t+1e-5)) + 1e-5))
    return _log_template

def polynomial_template(a, b, c, d, e, f, g):
    def _polynomial_template(x, y):
        return a*x**6 + b*x**5 + c*x**4 + d*x**3 + e*x**2 + f*x + g
    return _polynomial_template

if __name__ == '__main__':
    # Create a random graph with N = 1000 vertices
    g = graph.erdos_renyi(1000, 1.8)
    # Create a colouring with q = 750 and a beta function
    # c = Colouring.Colouring(g, 550, beta)
    # # number of iterations
    # iter_num = int(2e5)
    # # plot the results using the poor-man's plot
    # CMDPlot.command_line_plot(c.metropolis(iter_num), x_precision=120, y_precision=60)

    sys.stderr.write(">> Generated Erdos-Renyi graph with N=1,000 and c=1.8\n")
    sys.stderr.write(">> Trying bandit with exponential template \n")
    sys.stderr.write(">>>> q = 350 with 1,000,000 iterations with 10,000 training iterations\n")
    exp_bandit = bandit.BanditBeta(g, 35, exp_template, 3, metropolis_iter=1e6,
            initial_assignments=[random(), random(), random()], log=True)
    exp_bandit.train(10000)
    sys.stderr.write("\n>>>> Optimal variables: %s\n" % exp_bandit.variables)
    sys.stderr.write(">>>> Optimal loss: %s\n\n" % exp_bandit.min_loss)

    sys.stderr.write(">> Trying bandit with log template \n")
    sys.stderr.write(">>>> q = 350 with 1,000,000 iterations with 10,000 training iterations\n")
    log_bandit = bandit.BanditBeta(g, 35, log_template, 3, metropolis_iter=1e6,
            initial_assignments=[random(), random(), random()], log=True)
    log_bandit.train(10000)
    sys.stderr.write("\n>>>> Optimal variables: %s\n" % log_bandit.variables)
    sys.stderr.write(">>>> Optimal loss: %s\n\n" % log_bandit.min_loss)

    sys.stderr.write(">> Trying bandit with polynomial template \n")
    sys.stderr.write(">>>> q = 350 with 1,000,000 iterations with 10,000 training iterations\n")
    pol_bandit = bandit.BanditBeta(g, 35, polynomial_template, 7, metropolis_iter=1e6,
            initial_assignments=[random(), random(), random(), random(), random(), random(), random()], log=True)
    pol_bandit.train(10000)
    sys.stderr.write("\n>>>> Optimal variables: %s\n" % pol_bandit.variables)
    sys.stderr.write(">>>> Optimal loss: %s\n\n" % pol_bandit.min_loss)
