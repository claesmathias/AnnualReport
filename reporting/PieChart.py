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


    def create(self):
        # Sort the list by year
        self.list = sorted(self.list, key=lambda item: item.Info['Year'])

        # Iterate over the list
        for item in self.list:
            # Add operating cost, total inclusive
            Utilities.set_dictionary(self.var.operating_cost, item.Operations.OperatingCosts)


        figure()

        # The slices will be ordered and plotted counter-clockwise.
        slices = {'Sales': 0, 'RD': 0, 'General': 0, 'Amortization': 0}

        # last element represents last year (ordered list)
        last_year_total_operating_cost = (self.var.operating_cost['Total'])[-1]

        # calculate all slices
        for key in slices.keys():
            # last element represents last year (ordered list)
            last_year_operating_cost = (self.var.operating_cost[key])[-1]
            slices[key] = last_year_operating_cost / last_year_total_operating_cost

        # Sort the list by value
        #slices = sorted(slices.items(), key=operator.itemgetter(1))

        # only "explode" the 2nd slice
        explode = (0, 0.1, 0, 0)

        fig = plt.figure(figsize=[10, 10])
        ax = fig.add_subplot(111)

        # Make a pie chart
        pie_wedge_collection = ax.pie(
            [float(v) for v in slices.values()],         # [expression for target in iterable]
            explode=explode,
            colors=[str(v) for v in self.Settings.colors.values()],
            labels=list(slices),
            labeldistance=1.05,
            autopct='%1.1f%%',
            shadow=True,
            startangle=90)

        for pie_wedge in pie_wedge_collection[0]:
            pie_wedge.set_edgecolor('white')

        plt.title(self.Settings.title)

        plt.savefig(self.Settings.title + '.png')