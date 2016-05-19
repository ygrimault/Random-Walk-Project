"""
    This simple module implements a function that can plot data to a command
    line. Might be faster than waiting for a gui instance to load and plot
    the data. The plotter is a very crude one.
"""


def command_line_plot(history, x_precision=1, y_precision=20, x_start=0):
    """
    A poor man's plot. Plot data on the command line.

    :param history: An array of numerical values to plot.
                    The index is plotted on the horizontal axis and the value on
                    the vertical axis
    :param x_precision: How many ticks to show on the horizontal axis.
    :param y_precision: How many ticks to show on the vertical axis.
    :param x_start: From which point in the history the plotting should start.
    """
    whole_max = max(history)
    whole_min = min(history)

    history = history[x_start:]
    max_entry = max(history)
    min_entry = min(history)

    y_step = int((max_entry - min_entry) / y_precision)+1
    x_step = int(len(history) / x_precision)

    # plot the y axis and the data
    for y in range(int(min_entry), int(max_entry)+2, y_step)[::-1]:
        print('%10d |' % y, end='')
        for i in range(0, len(history), x_step):
            h = history[i]
            print('*' if y <= h < y+y_step else ' ', end='')
        print()

    # plot the x axis
    print(' '*11 + '-'*(x_precision+1))
    print(' '*12, end='')

    for t in range(0, len(history), x_step):
        if t/x_step % 10 == 0:
            label = '%d' % t
            print(label.ljust(10, ' '), end='')

    print("(+%d)" % x_start)
    print("min/max y: %d, %d" % (whole_min, whole_max))
