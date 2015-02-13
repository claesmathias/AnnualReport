__author__ = 'claesmathias'


from pylab import *
import numpy as np
from collections import OrderedDict
from Utilities import Utilities
import operator


class PieChart():

    class Settings():
        # plot details
        title = 'Operating Expenses'
        colors = \
            {'Sales': 'lightcoral', 'RD': 'lightskyblue', 'General': 'orange',
             'Amortization': 'gold'}

    class Slice:
        def __init__(self, label, color, value):
            self.label = label
            self.color = color
            self.value = value

    class Variables:
        def __init__(self):
            self.sales = []
            self.rd = []
            self.general = []
            self.amortization = []
            self.total = []
            self.operating_cost = \
                {'Sales': self.sales, 'RD': self.rd, 'General': self.general,
                 'Amortization': self.amortization, 'Total': self.total}

    def __init__(self, list):
        self.list = list
        self.var = self.Variables()
        self.slices = [
            self.Slice('Sales', self.Settings.colors['Sales'], 0),
            self.Slice('RD', self.Settings.colors['RD'], 0),
            self.Slice('General', self.Settings.colors['General'], 0),
            self.Slice('Amortization', self.Settings.colors['Amortization'], 0),
        ]


    def create(self):
        # Sort the list by year
        self.list = sorted(self.list, key=lambda item: item.Info['Year'])

        # Iterate over the list
        for item in self.list:
            # Add operating cost, total inclusive
            Utilities.set_dictionary(self.var.operating_cost, item.Operations.OperatingCosts)

        # last element represents last year (ordered list)
        last_year_total_operating_cost = (self.var.operating_cost['Total'])[-1]

        # calculate all slices
        for slice in self.slices:
            # last element represents last year (ordered list)
            last_year_operating_cost = (self.var.operating_cost[slice.label])[-1]
            slice.value = last_year_operating_cost / last_year_total_operating_cost

        # Sort the list by value
        slices = sorted(self.slices, key=lambda slice: slice.value, reverse=True)

        # only "explode" the 2nd slice
        explode = (0, 0.1, 0, 0)

        # Create new figure
        fig = plt.figure(figsize=[10, 10])
        ax = fig.add_subplot(111)

        # The slices will be ordered and plotted counter-clockwise.
        # Make a pie chart
        pie_wedge_collection = ax.pie(
            [float(s.value) for s in slices],         # [expression for target in iterable]
            explode=explode,
            colors=[s.color for s in slices],
            labels=[s.label for s in slices],
            labeldistance=1.05,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90)

        for pie_wedge in pie_wedge_collection[0]:
            pie_wedge.set_edgecolor('white')

        # Set plot title
        plt.title(self.Settings.title)

        # Save figure as *.PNG
        fig.savefig(self.Settings.title.replace(" ", "_") + '.png')

        # Save figure as *.PGF
        fig.savefig(self.Settings.title.replace(" ", "_") + '.pgf')
