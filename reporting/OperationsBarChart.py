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
from collections import OrderedDict
from Utilities import Utilities
from Reporting import *


class OperationsBarChart():

    class Settings:
        # plot details
        title = 'Statements of Operations Data'
        bar_width = 0.35/2
        epsilon = .015
        line_width = 1
        opacity = 0.7
        colors = \
            {'Gross Profit': 'green', 'COGS': 'white', 'Revenue': 'green',
             'Gross Profit Margin': 'r', 'Profit Margin': 'b', 'Operating Profit Margin': 'g',
             'Sales': 'lightcoral', 'RD': 'lightskyblue', 'General': 'orange',
             'Amortization': 'gold'}

    class Variables:
        def __init__(self):
            self.t = []
            self.revenue = []
            self.cost_goods = []
            self.sales = []
            self.rd = []
            self.general = []
            self.amortization = []
            self.net_income = []
            self.total_operating_cost = []
            self.operating_cost = \
                {'Sales': self.sales, 'RD': self.rd, 'General': self.general,
                 'Amortization': self.amortization}

    def __init__(self, list):
        self.list = list
        self.var = self.Variables()

    def create(self):

        if isinstance(self.list[0], AnnualReport):
            # Sort the list by year
            self.list = sorted(self.list, key=lambda item: item.Info['Year'])
        elif isinstance(self.list[0], QuarterlyEarnings):
            # Sort the list by year
            self.list = sorted(self.list, key=lambda item: (item.Info['Year'], item.Info['Quarter']))

        # Iterate over the list
        for item in self.list:
            if isinstance(self.list[0], AnnualReport):
                self.var.t.append(
                    item.Info['Year'])
            elif isinstance(self.list[0], QuarterlyEarnings):
                if item.Info['Quarter'] == "Q1":
                    self.var.t.append(
                        item.Info['Quarter'] + " " + item.Info['Year'])
                else:
                    self.var.t.append(
                        item.Info['Quarter'])
            self.var.revenue = np.append(
                self.var.revenue,
                int(item.Operations.Revenue))
            self.var.cost_goods = np.append(
                self.var.cost_goods,
                int(item.Operations.CostGoodsSold))
            self.var.net_income = np.append(
                self.var.net_income,
                int(item.Operations.NetIncome))
            self.var.total_operating_cost = np.append(
                self.var.total_operating_cost,
                int(item.Operations.OperatingCosts['Total']))

            # Add operating cost
            Utilities.set_dictionary(self.var.operating_cost, item.Operations.OperatingCosts)

        # Create label formatter
        format_to_millions = FuncFormatter(Utilities.to_millions)

        #
        # Create plots
        #
        fig, ax = plt.subplots()
        x = np.arange(len(self.var.revenue))

        ax.set_color_cycle(['r', 'g', 'b', 'y'])

        #
        # Sub plot 1: Make bar plot
        width = self.Settings.bar_width
        offset = 1.75 * width

        # Gross Profit
        gross_profit = self.var.revenue - self.var.cost_goods

        ax.bar(
            x + offset,                                         # value
            gross_profit,                                       # np.array
            width,                                              # bar width
            color=self.Settings.colors['Gross Profit'],         # color
            edgecolor=self.Settings.colors['Revenue'],          # edge color
            label="Gross Profit")                               # label

        ax.bar(
               x + offset,                                      # value
               self.var.cost_goods,                             # np.array
               width,                                           # bar width
               bottom=gross_profit,                             # bottom
               color=self.Settings.colors['COGS'],              # color
               edgecolor=self.Settings.colors['Revenue'],       # edge color
               linewidth=self.Settings.line_width,              # line width
               hatch='//',                                      # hatch
               label="COGS")                                    # label

        # reset bottom
        total_bottom = 0

        offset = 3.25 * width

        sorted_operating_cost = OrderedDict(sorted(self.var.operating_cost.items(), key=lambda t: (t[1])[-1], reverse=True))


        # Iterate over all the operating cost
        for key in sorted_operating_cost.keys():

            # add a bar to the plot
            ax.bar(
                x + offset,                                 # value
                self.var.operating_cost[key],               # np.array
                width,                                      # bar width
                total_bottom,                               # bottom value
                color=self.Settings.colors[key],            # color
                edgecolor=self.Settings.colors[key],        # edge color
                label=key)                                  # label

            # add item to the bottom count
            total_bottom += self.var.operating_cost[key]

        hunderd_million = 100000
        y1_min = 0        # 0 million
        y1_max = math.ceil(1.1*max(self.var.revenue)/hunderd_million) * hunderd_million
        y1_ticks = 10     # number of ticks

        # Set y1 limits and ticks
        step = (y1_max-y1_min)/y1_ticks
        ax.set_ylim([y1_min, y1_max])
        ax.yaxis.set_ticks(np.arange(y1_min, y1_max+step, step))

        #
        # Sub plot 2: Make scatter plot
        ax2 = ax.twinx()

        offset = 3 * width
        gross_profit_margin = gross_profit / self.var.revenue
        profit_margin = self.var.net_income / self.var.revenue
        operating_profit_margin = \
            (gross_profit - self.var.total_operating_cost) / self.var.revenue

        labels_values = {'Gross Profit Margin': gross_profit_margin,
                         'Operating Profit Margin': operating_profit_margin,
                         'Profit Margin': profit_margin}

        for key in labels_values.keys():

            ax2.plot(
                x+offset,                                       # x value
                labels_values[key],                             # y value
                self.Settings.colors[key],                      # color
                label=key)                                      # label

            ax2.plot(
                x+offset,                                       # x value
                labels_values[key],                             # y value
                self.Settings.colors[key] + 'o',                # color
                markeredgecolor=self.Settings.colors[key])      # marker edge color


        y2_min = 0.0                            # 0%
        y2_max = 1.0                            # 100%
        y2_ticks_major = y1_ticks               # 10 ticks, same as y1
        y2_ticks_minor = y2_ticks_major * 2     # 20 ticks

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

        # Create the formatter using the function to_percent. This multiplies all the
        # default labels by 100, making them all percentages
        format_to_percent = FuncFormatter(Utilities.to_percent)

        # Set format for y1 and y2
        ax2.yaxis.set_major_formatter(format_to_percent)
        ax.yaxis.set_major_formatter(format_to_millions)

        offset = 3 * width
        plt.xticks(x + offset, self.var.t)

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