__author__ = 'claesmathias'


# Effective Tax Rate
# Return on assets
# Return on equity
# Return on capital employed

# OTHER: Current Ratio


from pylab import *
import numpy as np


class ProfitabilityIndicators():

    class Settings:
        # plot details
        figure = 'Profitability Indicators '
        title = {'Effective Tax Rate': 'Effective Tax Rate'}
        bar_width = 0.35/2

    class Variables:
        def __init__(self):
            self.t = []
            self.operating_income = []
            self.provision_income_taxes = []

    def __init__(self, list):
        self.list = list
        self.var = self.Variables()

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
            self.var.operating_income = np.append(
                self.var.operating_income,
                int(item.Operations.OperatingIncome['Total']))
            self.var.provision_income_taxes = np.append(
                self.var.provision_income_taxes,
                int(item.Operations.ProvisionIncomeTaxes))

        effective_tax_rate = self.var.provision_income_taxes / self.var.operating_income

        x = np.arange(len(self.var.provision_income_taxes))

        # Bar width
        width = self.Settings.bar_width
        offset = 2.5 * width

        # Create the formatter using the function to_percent. This multiplies all the
        # default labels by 100, making them all percentages
        format_to_percent = FuncFormatter(self.to_percent)

        # Create figure
        fig = plt.Figure()
        fig.set_canvas(plt.gcf().canvas)

        y_min = math.floor(0.80*min(effective_tax_rate*100))/100
        y_max = math.ceil(1.10*max(effective_tax_rate)*100)/100

        #
        # Sub plot 1: Scatter plot
        #
        ax = plt.subplot(2, 1, 1)
        ax.plot(x + offset, effective_tax_rate, 'bo-')
        plt.title(self.Settings.title['Effective Tax Rate'])
        plt.ylabel('Percentage')
        plt.xticks(x + offset, self.var.t)

        # Set y limits
        ax.set_ylim([y_min, y_max])

        # Set format for y axis
        ax.yaxis.set_major_formatter(format_to_percent)

        # Show plot
        #plt.show()

        # Save figure as *.PNG
        fig.savefig(self.Settings.figure + '.png')

        #plt.subplot(2, 1, 2)
        #plt.plot(x2, y2, 'r.-')
        #plt.xlabel('time (s)')
        #plt.ylabel('Undamped')