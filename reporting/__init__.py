__author__ = 'claesma1'


import os, glob
from Cheetah.Template import Template
from XMLParser import XMLParser
from Reporting import *
from OperationsBarChart import OperationsBarChart
from PieChart import PieChart
from OperatingPerformanceBarChart import OperatingPerformanceBarChart
from ProfitabilityIndicators import ProfitabilityIndicators


class author:
    name = "Mathias Claes"

class paper:
    title = OperationsBarChart.Settings.title


def main():
    # Create an object list
    list = []

    # Find all the annual reports in the current directory
    for file in glob.glob("annual_report_*.xml"):
        # Parse the first file found
        XMLParser(file).parse(list)

    annual_reports = [item for item in list if isinstance(item, AnnualReport)]
    quarterly_earnings = [item for item in list if isinstance(item, QuarterlyEarnings) and int(item.Info['Year']) >= 2013]

    # Sort the list by year
    # list = sorted(list, key=lambda item: item.Info['Year'])

    # Create new bar chart
    OperationsBarChart(annual_reports).create()
    obj = OperationsBarChart(quarterly_earnings)
    obj.Settings.title += " Quarterly Earnings"
    obj.create()

    # Create new pie char
    PieChart(annual_reports).create()

    # Create new horizontal bar char
    OperatingPerformanceBarChart(annual_reports).create()

    # Create
    ProfitabilityIndicators(annual_reports).create()

    # Create LaTeX report from template
    f = open('report.tex', 'w')
    t = Template(file="report.tmpl", searchList=[{'author': author(), 'paper': paper()}])
    f.write(str(t))


if __name__ == "__main__":
    main()