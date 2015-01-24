__author__ = 'claesmathias'


from pylab import *
import numpy as np
import plotly.plotly as py
from collections import OrderedDict
from Utilities import Utilities


class BarChart():

    class Settings:
        # plot details
        title = 'Statements of Operations Data'
        bar_width = 0.35/2
        epsilon = .015
        line_width = 1
        opacity = 0.7
        colors = \
            {'Gross Profit': 'green', 'COGS': 'white',
             'Gross Profit Margin': 'r', 'Profit Margin': 'b',
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
            self.total = []
            self.net_income = []
            self.operating_cost = \
                {'Sales': self.sales, 'RD': self.rd, 'General': self.general,
                 'Amortization': self.amortization}

    def __init__(self, list):
        self.list = list
        self.var = self.Variables()


    @staticmethod
    def to_millions(x, pos):
        'The two args are the value and tick position'
        return '$%1.1fM' % (x*1e-3)

    @staticmethod
    def to_percent(y, position):
        # Ignore the passed in position. This has the effect of scaling the default
        # tick locations.
        s = str(100 * y)

        # The percent symbol needs escaping in latex
        if matplotlib.rcParams['text.usetex'] == True:
            return s + r'$\%$'
        else:
            return s + '%'

    def create(self):
        # Sort the list by year
        self.list = sorted(self.list, key=lambda item: item.Info['Year'])

        # Iterate over the list
        for item in self.list:
            self.var.t.append(
                item.Info['Year'])
            self.var.revenue = np.append(
                self.var.revenue,
                int(item.Operations.Revenue))
            self.var.cost_goods = np.append(
                self.var.cost_goods,
                int(item.Operations.CostGoodsSold))
            self.var.net_income = np.append(
                self.var.net_income,
                int(item.Operations.NetIncome))

            # Add operating cost
            Utilities.set_dictionary(self.var.operating_cost, item.Operations.OperatingCosts)

        # Create label formatter
        format_to_millions = FuncFormatter(self.to_millions)

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
            x + offset,                                     # value
            gross_profit,                                   # np.array  ? revenue
            width,                                          # bar width
            color=self.Settings.colors['Gross Profit'],     # color
            label="Gross Profit")                           # label

        ax.bar(
               x + offset,                                  # value
               self.var.cost_goods,                         # np.array
               width,                                       # bar width
               bottom=gross_profit,                         # bottom
               color=self.Settings.colors['COGS'],          # color
               edgecolor='green',                           # edge color
               linewidth=self.Settings.line_width,          # line width
               hatch='//',                                  # hatch
               label="COGS")                                # label

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
                label=key)                                  # label

            # add item to the bottom count
            total_bottom += self.var.operating_cost[key]

        hunderd_million = 100000
        y1_min = 0        # 0 million
        y1_max = math.ceil(1.15*max(self.var.revenue)/hunderd_million) * hunderd_million;
        y1_ticks = 10     # number of ticks

        ax.set_ylim([y1_min, y1_max])
        ax.yaxis.set_ticks(np.arange(y1_min, y1_max, y1_max/y1_ticks))

        #
        # Sub plot 2: Make scatter plot
        ax2 = ax.twinx()

        offset = 3 * width
        gross_profit_margin = gross_profit / self.var.revenue
        profit_margin = self.var.net_income / self.var.revenue

        ax2.plot(
            x+offset,                                           # x value
            gross_profit_margin,                                # y value
            self.Settings.colors['Gross Profit Margin'],        # color
            label="Gross Profit Margin")                        # label

        ax2.plot(
            x+offset,                                           # x value
            gross_profit_margin,                                # y value
            self.Settings.colors['Gross Profit Margin'] + 'o')  # color

        ax2.plot(
            x+offset,                                           # x value
            profit_margin,                                      # y value
            self.Settings.colors['Profit Margin'],              # color
            label="Profit Margin")                              # label

        ax2.plot(
            x+offset,                                           # x value
            profit_margin,                                      # y value
            self.Settings.colors['Profit Margin'] + 'o')        # color

        y2_min = 0.0                    # 0%
        y2_max = 1.0                    # 100%
        y2_ticks_major = y1_ticks       # 10 ticks, same as y1
        y2_ticks_minor = y1_ticks * 2   # 20 ticks

        # ax2.set_ylabel('%')

        # Set y2 limits and ticks
        ax2.set_ylim([y2_min, y2_max])
        ax2.yaxis.set_ticks(np.arange(y2_min, y2_max, y2_max/y2_ticks_major))
        ax2.set_yticks(np.arange(y2_min, y2_max, y2_max/y2_ticks_minor), minor = True)

        # Set grids
        ax2.yaxis.grid(True, which='major')
        ax2.yaxis.grid(True, which='minor')

        # Create the formatter using the function to_percent. This multiplies all the
        # default labels by 100, making them all percentages
        format_to_percent = FuncFormatter(self.to_percent)

        # Set format for y1 en y2
        ax2.yaxis.set_major_formatter(format_to_percent)
        ax.yaxis.set_major_formatter(format_to_millions)

        offset = 3 * width
        plt.xticks(x + offset, self.var.t)

        # Set legend position
        ax.legend(loc='upper left', prop={'size':10})
        ax2.legend(loc='upper right', prop={'size':10})

        # Set title
        plt.title(self.Settings.title)

        # Show plot
        #plt.show()

        # Save figure as *.PNG
        fig.savefig(self.Settings.title + '.png')