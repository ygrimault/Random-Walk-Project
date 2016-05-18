from math import exp
from scipy import stats
from Colouring import Colouring
import sys
from statistics import median
import random

try:
    import progressbar
except ImportError:
    progressbar = None


class BanditBeta:

    @staticmethod
    def _lambda_change_ith_coefficient(i, v):
        """
        Generates a lambda that when invoked on a set of coefficients will
        increment the i-th one by v

        :param i: the i-th coefficient
        :param v: the additive constant to add to the i-th coefficient

        :return: lambda : \R^{degree+1} -> \R^{degree+1}
        """
        return lambda arr: \
            [x + int(j == i)*v for j, x in enumerate(arr)]

    def __init__(self, graph, number_colours, metropolis_iter=1e5, degree=6, log=True):
        """
        Create the bandit instance with a polynomial of a given degree.
        There will be 2*degree+2 arms, each will either increase or decrease
        a coefficient with a value of 0.1/i! where i is the i-th power
        corresponding to that coefficient.

        :param graph: graph on which to do the colouring
        :param number_colours: number of colours to colour the graph
        :param metropolis_iter: number of iterations to run the metropolis algorithm on
        :param degree: the degree of the polynomial
        :param log: whether or not to log the process of learning
        """
        self.graph = graph
        self.number_colours = number_colours
        self.metropolis_iter = metropolis_iter
        self.log = log  # Whether or not to log the process
        self.degree = degree
        self.coefficients = [1] * (degree+1)
        self.arms = []
        self.weights = [1.0] * (2*degree+2)
        for i in range(len(self.weights)):
            v = (-1) ** i * 0.2
            self.arms.append(self._lambda_change_ith_coefficient(int(i/2), v))

        self.min_loss = float('inf')  # the minimum loss found so far
        self.min_coefficients = []  # ^ its corresponding coefficients

    def loss(self, j):
        """
        Compute the loss produced by choosing the j-th arm.
        The loss of an arm is the following: (We can maybe choose a different one)
        The first time the minimum value is attained / number of iterations.

        :param j: the index of the arm selected
        :return: l \in [0, 1] (Needed to have a guarantee on the convergence)
        """
        self.coefficients = self.arms[j](self.coefficients)
        new_beta = self.get_polynomial()
        losses = []
        for _ in range(10):
            c = Colouring(self.graph, int(self.number_colours), new_beta)
            history = c.metropolis(int(self.metropolis_iter))
            losses.append(history.index(min(history))/len(history))
        return median(losses)

    def step(self):
        """
        Performs one step of the EXP3 algorithm:
            1. Convert the weights into a distribution
            2. Account for the exploration factor in the distribution
            3. Pick an arm based on this distribution
            4. Compute the loss produced by this arm and update its weight
        """
        phi = sum(self.weights)
        n = len(self.weights)
        # the factor of exploration, i.e. with probability 1/2n it will try new arms
        eps = (1.0/n)*0.5
        # distribution of picking arm
        distribution = list(map(lambda w: (1-n*eps)*w/phi + eps, self.weights))
        # random variable with the distribution above
        rv = stats.rv_discrete(values=(list(range(n)), distribution))
        j = rv.rvs()  # pick a random arm
        loss = self.loss(j)  # loss obtained by the arm
        self.weights[j] *= exp(-eps * loss)  # update its weight

        # We will always keep a copy of the "best" polynomial, that is the one
        # that gave the smallest loss. And carry on from it.
        if loss < self.min_loss:
            self.min_coefficients = self.coefficients
            self.min_loss = loss
        # With 99% of the time switch back to the original coefficients
        elif random.random() > 0.01:
            self.coefficients = self.min_coefficients

        if self.log:
            formatted_dist = ', '.join(list(map(lambda x: '%.3e' % x, distribution)))
            print(("Information about step:\n\t%d arms\n\thaving these weights: %s" +
                   "\n\tExploration factor: %f\n\tDistribution: %s\n\tExpert Picked: " +
                   "%d\n\tLoss: %f\n\tOptimal loss: %f\n\tUsing polynomial: %s")
                  % (n, str(self.weights), eps, formatted_dist, j, loss, self.min_loss, str(self)))

    def train(self, training_length):
        """
        Trains the Bandit for a given number of iterations

        :param training_length: Number of iterations to perform
        """
        if progressbar and self.log:
            bar = progressbar.ProgressBar(redirect_stdout=True)
            for _ in bar(range(training_length)):
                self.step()
        else:
            for i in range(training_length):
                if self.log:
                    block_len = (1.0*i/training_length)*60
                    output = "#"*int(block_len)
                    sys.stderr.write("\r%.2f%% [%s] (%d/%d) "
                                     % (100.0*i/training_length, output.ljust(60, ' '), i, training_length))
                self.step()

    def get_polynomial(self):
        """
        Returns a lambda representation of the polynomial

        :return: lambda: \R -> \R
        """
        return lambda x, _: \
            sum(map(lambda y: y[1] * x ** y[0],
                    enumerate(self.coefficients)))

    def __repr__(self):
        """
        Outputs a representation of the polynomial

        :return: string
        """
        return ' '.join(map(lambda x:
                            ('+ ' if x[1] >= 0 else '- ') +
                            (str(abs(x[1])) if abs(x[1]) != 1 else '') +
                            ('x^' + str(x[0]) if x[0] > 0 else ('1' if abs(x[1]) == 1 else '')),
                            enumerate(self.coefficients)))
