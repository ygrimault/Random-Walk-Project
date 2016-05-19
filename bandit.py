from math import exp
from scipy import stats
from colouring import Colouring
import sys
from statistics import median
import random

try:
    import progressbar
except ImportError:
    progressbar = None


class BanditBeta:

    @staticmethod
    def _lambda_change_ith_variable(i, v):
        """
        Generates a lambda that when invoked on a set of variables will
        increment the i-th one by v

        :param i: the i-th variable
        :param v: the additive constant to add to the i-th variable

        :return: lambda : \R^{degree+1} -> \R^{degree+1}
        """
        return lambda arr: \
            [x*v for j, x in enumerate(arr)]

    def __init__(self, graph, number_colours, function_template, num_variables,
            metropolis_iter=1e5, log=True, initial_assignments=[]):
        """
        Create the bandit instance with a function template and its variables.
        There will be 2*num_variables arms, each will either increase or decrease
        a variable by 10%

        :param graph: graph on which to do the colouring
        :param number_colours: number of colours to colour the graph
        :param function_template: a function which given some variables returns a function
            that given a real returns a real, i.e. a template of the function
        :param metropolis_iter: number of iterations to run the metropolis algorithm on
        :param num_variables: the number of free variables to optimize over
        :param log: whether or not to log the process of learning
        """
        self.graph = graph
        self.number_colours = number_colours
        self.function_template = function_template
        self.metropolis_iter = metropolis_iter
        self.log = log
        self.num_variables = num_variables
        self.variables = [1] * num_variables if len(initial_assignments) == 0 else initial_assignments
        self.arms = []
        self.weights = [1.0] * (2*num_variables)
        print(self.variables)
        for i in range(len(self.weights)):
            v = 1 + (-1) ** i * 0.1
            self.arms.append(self._lambda_change_ith_variable(int(i/2), v))

        self.min_loss = float('inf')  # the minimum loss found so far
        self.min_variables = []  # ^ its corresponding variables

    def loss(self, j):
        """
        Compute the loss produced by choosing the j-th arm.
        The loss of an arm is the following: (We can maybe choose a different one)
        The first time the minimum value is attained / number of iterations.
        This function runs 5 trials and chooses the median of the losses found

        :param j: the index of the arm selected
        :return: l \in [0, 1] (Needed to have a guarantee on the convergence)
        """
        self.variables = self.arms[j](self.variables)
        new_beta = self.get_function()
        losses = []
        for _ in range(5):
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

        # We will always keep a copy of the "best" varialbles, that is the one
        # that gave the smallest loss. And carry on from it.
        if loss < self.min_loss:
            self.min_variables = self.variables
            self.min_loss = loss
        # With 99% of the time switch back to the original variables when the
        # loss is not too much higher than the minimum one found (0.1)
        elif random.random() > 0.01 and loss - self.min_loss >= 0.1:
            self.variables = self.min_variables

        if self.log:
            formatted_dist = ', '.join(list(map(lambda x: '%.3e' % x, distribution)))
            print(("Information about step:\n\t%d arms\n\thaving these weights: %s" +
                   "\n\tExploration factor: %f\n\tDistribution: %s\n\tExpert Picked: " +
                   "%d\n\tLoss: %f\n\tOptimal loss: %f\n\tUsing variables: %s\n\t"+
                   "With minimal variables: %s")
                   % (n, str(self.weights), eps, formatted_dist, j, loss, self.min_loss,
                       str(self), str(self.min_variables)))

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
                block_len = (1.0*i/training_length)*60
                output = "#"*int(block_len)
                sys.stderr.write("\r%.2f%% [%s] (%d/%d) "
                                 % (100.0*i/training_length, output.ljust(60, ' '), i, training_length))
                self.step()

    def get_function(self):
        """
        Returns a function which is the function template provided filled with
        the variables

        :return: lambda: \R -> \R
        """
        return self.function_template(*self.variables)

    def __repr__(self):
        """
        Outputs a representation of the variables

        :return: string
        """
        return str(self.variables)
