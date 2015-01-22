__author__ = 'claesma1'


import os, glob
import xml.etree.ElementTree as ET
from AnnualReport import AnnualReport
from pylab import *
import numpy as np
import plotly.plotly as py


def millions(x, pos):
    'The two args are the value and tick position'
    return '$%1.1fM' % (x*1e-3)

def main():
    # Create an object list
    list = []

    # Find all the annual reports in the current directory
    for file in glob.glob( "annual_report_*.xml" ):
        # Parse the first file found
        tree = ET.parse( file )

        # Get the XML root
        root = tree.getroot()

        # Find the 'Report' tag
        for report in root.findall( 'Report' ):
            # Create a new annual report
            ar = AnnualReport()

            ## Parse the info statement
            info = report.find( 'Info' )
            ar.Info.Year = info.find( 'Year' ).text
            ar.Info.Employees = info.find( 'Employees' ).text

            ## Parse the Consolidated Balance Sheets
            balance = report.find( 'Balance' )
            assets = balance.find( 'Assets' )
            # Parse the current assets
            currentAssets = assets.find( 'CurrentAssets' )
            ca = ar.Balance.Assets.CurrentAssets
            ca.Cash = currentAssets.find( 'Cash' ).text
            ca.Total = currentAssets.find( 'Total' ).text
            # Parse the non-current assets

            # Parse the Consolidated Statements of Operations Data
            operations = report.find( 'Operations' )
            o = ar.Operations
            o.Revenue = operations.find( 'Revenue' ).text
            o.CostGoodsSold = operations.find( 'CostGoodsSold' ).text
            # Parse the operating costs
            operatingCosts = operations.find( 'OperatingCosts' )
            oc = ar.Operations.OperatingCosts
            oc.Sales = operatingCosts.find( 'Sales' ).text
            oc.RD = operatingCosts.find( 'RD' ).text
            oc.General = operatingCosts.find( 'General' ).text
            oc.Amortization = operatingCosts.find( 'Amortization' ).text

            # Add the new annual report to the list
            list.append( ar )

    # Sort the list by year
    list = sorted(list, key=lambda item: item.Info.Year)


    t = []
    cash = []
    employees = []
    revenue = []
    costgoods = []
    sales = []
    rd = []
    general =[]
    amortization = []


    for item in list:
        t.append( item.Info.Year )
        cash.append( int(item.Balance.Assets.CurrentAssets.Cash) )
        employees.append( int(item.Info.Employees) )
        revenue.append( int(item.Operations.Revenue) )
        costgoods.append( int(item.Operations.CostGoodsSold) )
        sales.append( int(item.Operations.OperatingCosts.Sales) )
        rd.append( int(item.Operations.OperatingCosts.RD) )
        general.append(( int(item.Operations.OperatingCosts.General)) )
        amortization.append( int(item.Operations.OperatingCosts.Amortization) )

    print t

    # Plot
    fig, ax1 = plt.subplots()

    ax1.plot( t, cash, t, revenue, t, costgoods )

    ax2 = ax1.twinx()
    ax2.plot(t, employees, 'r-')

    plt.show()

    width = 0.35       # the width of the bars

    formatter = FuncFormatter(millions)
    fig, ax = plt.subplots()
    x = np.arange(len(cash))

    #rect1 = ax.bar(x, cash, width, color='r')
    rect2 = ax.bar(x, revenue, width, color='y')
    rect3 = ax.bar(x+width, sales, width, color='b')
    rect4 = ax.bar(x+width, rd, width, color='g', bottom=sales)
    rect5 = ax.bar(x+width, general, width, color='r', bottom=rd)
    rect5 = ax.bar(x+width, amortization, width, color='c', bottom=general)

    ax.yaxis.set_major_formatter(formatter)
    plt.xticks( x + 0.5, t )

    plt.show()

    py.sign_in('claesmathias', '92vee4drw8')
    plot_url = py.plot_mpl(fig)

    print plot_url



if __name__ == "__main__":
    main()