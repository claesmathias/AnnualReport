__author__ = 'claesmathias'


# Effective Tax Rate
# Return on assets
# Return on equity
# Return on capital employed
# Working capital ratio

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
from Utilities import Utilities


class ProfitabilityIndicators():

    class Settings:
        # plot details
        figure = 'Profitability Indicators'
        title = {'Effective Tax Rate': 'Effective Tax Rate',
                 'Return on ...': 'Return on ...',
                 "Ratio's": "Ratio's"}
        labels = {'ROA': 'ROA', 'ROE': 'ROE', 'ROC': 'ROC',
                  'Current Ratio': 'Current Ratio', 'Quick Ratio': 'Quick Ratio'}
        bar_width = 0.35/2

    class Variables:
        def __init__(self):
            self.t = []
            self.equity = []
            self.net_income = []
            self.total_assets = []
            self.operating_income = []
            self.total_operating_income = []
            self.provision_income_taxes = []
            self.total_current_liabilities = []
            self.total_current_assets = []
            self.inventories = []
            self.cash = []

    def __init__(self, list):
        self.list = list
        self.var = self.Variables()

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
                int(item.Operations.OperatingIncome['OperatingIncome']))
            self.var.total_operating_income = np.append(
                self.var.total_operating_income,
                int(item.Operations.OperatingIncome['Total']))
            self.var.provision_income_taxes = np.append(
                self.var.provision_income_taxes,
                int(item.Operations.ProvisionIncomeTaxes))
            self.var.equity = np.append(
                self.var.equity,
                int(item.Balance.Liabilities.StockholderEquity))
            self.var.total_current_assets = np.append(
                self.var.total_current_assets,
                int(item.Balance.Assets.CurrentAssets['Total']))
            self.var.total_current_liabilities = np.append(
                self.var.total_current_liabilities,
                int(item.Balance.Liabilities.CurrentLiabilities['Total']))
            self.var.inventories = np.append(
                self.var.inventories,
                int(item.Balance.Assets.CurrentAssets['Inventories']))
            self.var.cash = np.append(
                self.var.cash,
                int(item.Balance.Assets.CurrentAssets['Cash']))

        effective_tax_rate = self.var.provision_income_taxes / self.var.total_operating_income
        return_on_assets = ndarray((len(self.var.t)-1,), float)
        return_on_equity = ndarray((len(self.var.t)-1,), float)
        return_on_capital = ndarray((len(self.var.t)-1,), float)

        for i in range(1, len(self.var.net_income)):
            # Calculate return on assets (ROA)
            return_on_assets[i-1] = (2 * self.var.net_income[i]) / (self.var.total_assets[i-1] + self.var.total_assets[i])
            # Calculate return on equity (ROE)
            return_on_equity[i-1] = (2 * self.var.net_income[i]) / (self.var.equity[i-1] + self.var.equity[i])
            # Calculate return on capital (ROC)
            invested_capital = self.var.equity[i] - self.var.cash[i] # + long-term debt + short-term debt
            invested_capital_year_before = self.var.equity[i-1] - self.var.cash[i-1] # + long term debt + short term debt
            return_on_capital[i-1] = (2 * self.var.operating_income[i] * (1-effective_tax_rate[i])) / (invested_capital + invested_capital_year_before)

        current_ratio = self.var.total_current_assets / self.var.total_current_liabilities
        quick_ratio = (self.var.total_current_assets - self.var.inventories) / self.var.total_current_liabilities

        x = np.arange(len(self.var.provision_income_taxes))

        minor_locator = MultipleLocator(0.01)

        # Bar width
        width = self.Settings.bar_width
        offset = 2.5 * width

        # Create the formatter using the function to_percent. This multiplies all the
        # default labels by 100, making them all percentages
        format_to_percent = FuncFormatter(Utilities.to_percent)

        # Create figure
        fig1 = plt.figure(1)
        fig1.set_canvas(plt.gcf().canvas)

        #
        # Sub plot 1: Scatter plot
        #
        y_min = math.floor(0.80*min(effective_tax_rate*20))/20
        y_max = math.ceil(1.10*max(effective_tax_rate)*20)/20

        ax = plt.subplot(2, 1, 1)
        ax.plot(x + offset, effective_tax_rate, 'bo-')
        plt.title(self.Settings.title['Effective Tax Rate'])
        plt.ylabel('Percentage')
        plt.xticks(x + offset, self.var.t)

        # Set y limits
        ax.set_ylim([y_min, y_max])

        # Set format for y axis
        ax.yaxis.set_major_formatter(format_to_percent)
        ax.yaxis.set_minor_locator(minor_locator)

        #
        # Sub plot 2: Scatter plot
        #
        temp = [min(return_on_assets), min(return_on_equity)]
        sign = -1 if temp < 0 else 1
        y_min = sign * math.floor(0.80*abs(min(temp))*20)/20
        temp = [max(return_on_assets), max(return_on_equity)]
        sign = -1 if temp < 0 else 1
        y_max = sign * math.ceil(1.10*abs(max(temp))*20)/20


        ax = plt.subplot(2, 1, 2)
        ax.plot(x[1:] + offset, return_on_assets, 'bo-', label=self.Settings.labels["ROA"])
        ax.plot(x[1:] + offset, return_on_equity, 'ro-', label=self.Settings.labels["ROE"])
        plt.title(self.Settings.title['Return on ...'])
        plt.ylabel('Percentage')
        plt.xticks(x[1:] + offset, self.var.t[1:])

        # Set y limits
        ax.set_ylim([y_min, y_max])

        # Set format for y axis
        ax.yaxis.set_major_formatter(format_to_percent)
        ax.yaxis.set_minor_locator(minor_locator)

        # Set legend position
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00),
          ncol=3, fancybox=True, shadow=True)

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
        temp = [min(return_on_capital)]
        sign = -1 if temp < 0 else 1
        y_min = sign * math.floor(0.80*abs(min(temp))*20)/20
        temp = [max(return_on_capital)]
        sign = -1 if temp < 0 else 1
        y_max = sign * math.ceil(1.10*abs(max(temp))*20)/20

        ax = plt.subplot(2, 1, 1)
        ax.plot(x[1:] + offset, return_on_capital, 'go-', label=self.Settings.labels["ROC"])
        plt.title(self.Settings.labels["ROC"])
        plt.ylabel('Percentage')
        plt.xticks(x[1:] + offset, self.var.t[1:])

        # Set y limits
        ax.set_ylim([y_min, y_max])

        # Set format for y axis
        ax.yaxis.set_major_formatter(format_to_percent)
        ax.yaxis.set_minor_locator(minor_locator)


        #
        # Sub plot 2: Scatter plot
        #
        y_min = math.floor(0.80*min(min(current_ratio), min(quick_ratio), 1.0)*20)/20
        y_max = math.ceil(1.10*max(max(current_ratio), max(quick_ratio), 1.0)*20)/20

        minor_locator = MultipleLocator(0.1)

        ax = plt.subplot(2, 1, 2)
        ax.plot(x + offset, current_ratio, 'bo-', label=self.Settings.labels["Current Ratio"])
        ax.plot(x + offset, quick_ratio, 'ro-', label=self.Settings.labels["Quick Ratio"])
        ax.plot((min(x) - 2*offset, max(x) + 2*offset), (1.5, 1.5), 'g-')
        plt.title(self.Settings.title["Ratio's"])
        plt.ylabel('Percentage')
        plt.xticks(x + offset, self.var.t)

        # Set y limits
        ax.set_ylim([y_min, y_max])

        # Set format for y axis
        #ax.yaxis.set_major_formatter(format_to_percent)
        ax.yaxis.set_minor_locator(minor_locator)

        # Set legend position
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.00),
          ncol=3, fancybox=True, shadow=True)

        # Show plot
        #plt.show()

        # Save figure as *.PNG
        fig2.savefig(self.Settings.figure.replace(" ", "_") + '_2.png')

        # Save figure as *.PGF
        fig2.savefig(self.Settings.figure.replace(" ", "_") + '_2.pgf')