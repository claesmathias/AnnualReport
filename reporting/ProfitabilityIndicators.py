__author__ = 'claesmathias'


# Effective Tax Rate
# Return on assets
# Return on equity
# Return on capital employed

# OTHER: Current Ratio
# Acid Test ratio


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


class ProfitabilityIndicators():

    class Settings:
        # plot details
        figure = 'Profitability Indicators'
        title = {'Effective Tax Rate': 'Effective Tax Rate',
                 'Return on Assets': 'Return on Assets',
                 'Return on Equity': 'Return on Equity'}
        bar_width = 0.35/2

    class Variables:
        def __init__(self):
            self.t = []
            self.equity = []
            self.net_income = []
            self.total_assets = []
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
            self.var.net_income = np.append(
                self.var.net_income,
                int(item.Operations.NetIncome))
            self.var.total_assets = np.append(
                self.var.total_assets,
                int(item.Balance.Assets.Total))
            self.var.operating_income = np.append(
                self.var.operating_income,
                int(item.Operations.OperatingIncome['Total']))
            self.var.provision_income_taxes = np.append(
                self.var.provision_income_taxes,
                int(item.Operations.ProvisionIncomeTaxes))
            self.var.equity = np.append(
                self.var.equity,
                int(item.Balance.Liabilities.StockholderEquity))

        effective_tax_rate = self.var.provision_income_taxes / self.var.operating_income
        return_on_assets = self.var.net_income / self.var.total_assets
        return_on_equity = self.var.net_income / self.var.equity

        x = np.arange(len(self.var.provision_income_taxes))

        # Bar width
        width = self.Settings.bar_width
        offset = 2.5 * width

        # Create the formatter using the function to_percent. This multiplies all the
        # default labels by 100, making them all percentages
        format_to_percent = FuncFormatter(self.to_percent)

        # Create figure
        fig1 = plt.figure(1)
        fig1.set_canvas(plt.gcf().canvas)

        #
        # Sub plot 1: Scatter plot
        #
        y_min = math.floor(0.80*min(effective_tax_rate*100))/100
        y_max = math.ceil(1.10*max(effective_tax_rate)*100)/100

        ax = plt.subplot(2, 1, 1)
        ax.plot(x + offset, effective_tax_rate, 'bo-')
        plt.title(self.Settings.title['Effective Tax Rate'])
        plt.ylabel('Percentage')
        plt.xticks(x + offset, self.var.t)

        # Set y limits
        ax.set_ylim([y_min, y_max])

        # Set format for y axis
        ax.yaxis.set_major_formatter(format_to_percent)

        #
        # Sub plot 2: Scatter plot
        #
        y_min = math.floor(0.80*min(return_on_assets*100))/100
        y_max = math.ceil(1.10*max(return_on_assets)*100)/100

        ax = plt.subplot(2, 1, 2)
        ax.plot(x + offset, return_on_assets, 'bo-')
        plt.title(self.Settings.title['Return on Assets'])
        plt.ylabel('Percentage')
        plt.xticks(x + offset, self.var.t)

        # Set y limits
        ax.set_ylim([y_min, y_max])

        # Set format for y axis
        ax.yaxis.set_major_formatter(format_to_percent)

        # Show plot
        #plt.show()

        # Save figure as *.PNG
        fig1.savefig(self.Settings.figure.replace(" ", "_") + '_1.png')

        # Save figure as *.PGF
        fig1.savefig(self.Settings.figure.replace(" ", "_") + '_1.pgf')


        # Create figure
        fig2 = plt.figure(2)
        fig2.set_canvas(plt.gcf().canvas)

        #
        # Sub plot 1: Scatter plot
        #
        y_min = math.floor(0.80*min(return_on_equity*100))/100
        y_max = math.ceil(1.10*max(return_on_equity)*100)/100

        ax = plt.subplot(2, 1, 1)
        ax.plot(x + offset, return_on_equity, 'bo-')
        plt.title(self.Settings.title['Return on Equity'])
        plt.ylabel('Percentage')
        plt.xticks(x + offset, self.var.t)

        # Set y limits
        ax.set_ylim([y_min, y_max])

        # Set format for y axis
        ax.yaxis.set_major_formatter(format_to_percent)

        #
        # Sub plot 2: Scatter plot
        #

        # Show plot
        #plt.show()

        # Save figure as *.PNG
        fig2.savefig(self.Settings.figure.replace(" ", "_") + '_2.png')

        # Save figure as *.PGF
        fig2.savefig(self.Settings.figure.replace(" ", "_") + '_2.pgf')