__author__ = 'claesmathias'

import matplotlib as mpl
mpl.use("pgf")
pgf_with_pdflatex = {
    "pgf.texsystem": "pdflatex",
    "pgf.preamble": [
         r"\usepackage[utf8x]{inputenc}",
         r"\usepackage[T1]{fontenc}",
         r"\usepackage{cmbright}",
         ]
}
mpl.rcParams.update(pgf_with_pdflatex)

from pylab import *
import numpy as np
import matplotlib.pyplot as plt
from BarChartSettings import BarChartSettings


class OperatingPerformanceBarChart():

    class Settings(BarChartSettings):
        # plot details
        title = 'Operating Performance'
        colors = \
            {'Employees': 'green', 'Revenue Per Employee': 'r'}

    class Variables:
        def __init__(self):
            self.t = []
            self.employees = []
            self.revenue = []

    def __init__(self, list):
        self.list = list
        self.var = self.Variables()

    @staticmethod
    def to_thousand(x, pos):
        'The two args are the value and tick position'
        return '$%1.1fk' % (x)

    def create(self):

        # Sort the list by year
        self.list = sorted(self.list, key=lambda item: item.Info['Year'])

        # Iterate over the list
        for item in self.list:
            self.var.t.append(
                item.Info['Year'])
            self.var.employees = np.append(
                self.var.employees,
                int(item.Info['Employees']))
            self.var.revenue = np.append(
                self.var.revenue,
                int(item.Operations.Revenue))

        # Create label formatter
        format_to_thousand = FuncFormatter(self.to_thousand)

        #
        # Create plots
        #
        fig, ax = plt.subplots()
        x = np.arange(len(self.var.revenue))

        ax.set_color_cycle(['r', 'g', 'b', 'y'])

        #
        # Sub plot 1: Make bar plot
        width = self.Settings.bar_width
        offset = 2 * width

        ax.bar(
            x + offset,                                     # value
            self.var.employees,                             # np.array
            width,                                          # bar width
            color=self.Settings.colors['Employees'],      # color
            edgecolor=self.Settings.colors['Employees'],  # edge color
            label="Employees")                            # label

        y1_min = 0        # 0 million
        y1_max = math.ceil(1.15*max(self.var.employees)/100) * 100;
        y1_ticks = math.ceil(1.15*max(self.var.employees)/100)     # number of ticks

        # Set y1 limits and ticks
        step = (y1_max-y1_min)/y1_ticks
        ax.set_ylim([y1_min, y1_max])
        ax.yaxis.set_ticks(np.arange(y1_min, y1_max+step, step))

        #
        # Sub plot 2: Make scatter plot
        ax2 = ax.twinx()

        offset = 2.5 * width

        revenue_per_employee = self.var.revenue / self.var.employees

        label = 'Revenue Per Employee'

        print(self.Settings.colors[label])

        ax2.plot(
            x+offset,                                       # x value
            revenue_per_employee,                           # y value
            self.Settings.colors[label],                    # color
            label=label)                                    # label

        ax2.plot(
            x+offset,                                       # x value
            revenue_per_employee,                           # y value
            self.Settings.colors[label] + 'o',              # color
            markeredgecolor=self.Settings.colors[label])    # marker edge color

        y2_min = math.floor(0.85*min(revenue_per_employee)/100)*100
        y2_max = math.ceil(1.15*max(revenue_per_employee)/100)*100
        y2_ticks_major = y1_ticks # ticks
        y2_ticks_minor = y2_ticks_major * 2   # 20 ticks

        # ax2.set_ylabel('%')

        # Set y2 limits and ticks
        step_major = (y2_max-y2_min)/y2_ticks_major
        step_minor = (y2_max-y2_min)/y2_ticks_minor
        ax2.set_ylim([y2_min, y2_max])
        ax2.yaxis.set_ticks(np.arange(y2_min, y2_max+step_major, step_major))
        ax2.set_yticks(np.arange(y2_min, y2_max+step_minor, step_minor), minor=True)

        # Set grids
        ax2.yaxis.grid(True, which='major')
        ax2.yaxis.grid(True, which='minor')

        offset = 2.5 * width
        plt.xticks(x + offset, self.var.t)

        # Set format for y2
        ax2.yaxis.set_major_formatter(format_to_thousand)

        # Set legend position
        ax.legend(loc='upper left', prop={'size': 10})
        ax2.legend(loc='upper right', prop={'size': 10})

        # Set title
        plt.title(self.Settings.title)

        # Show plot
        #plt.show()

        # Save figure as *.PNG
        fig.savefig(self.Settings.title.replace(" ", "_") + '.png')

        # Save figure as *.PGF
        fig.savefig(self.Settings.title.replace(" ", "_") + '.pgf')

