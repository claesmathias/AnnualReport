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
        XMLParser(file).parse(list, None)

    # Sort the list by year
    # list = sorted(list, key=lambda item: item.Info['Year'])

    # Create new bar chart
    OperationsBarChart(list).create()

    # Create new pie char
    PieChart(list).create()

    # Create new horizontal bar char
    OperatingPerformanceBarChart(list).create()

    # Create
    ProfitabilityIndicators(list).create()

    # Create LaTeX report from template
    f = open('report.tex', 'w')
    t = Template(file="report.tmpl", searchList=[{'author': author(), 'paper': paper()}])
    f.write(str(t))


if __name__ == "__main__":
    main()