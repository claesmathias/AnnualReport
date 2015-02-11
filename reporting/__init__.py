__author__ = 'claesma1'


import os, glob
from XMLParser import XMLParser
from AnnualReport import AnnualReport
from OperationsBarChart import OperationsBarChart
from PieChart import PieChart
from OperatingPerformanceBarChart import OperatingPerformanceBarChart
from ProfitabilityIndicators import ProfitabilityIndicators


def main():
    # Create an object list
    list = []

    # Find all the annual reports in the current directory
    for file in glob.glob("annual_report_*.xml"):
        # Parse the first file found
        XMLParser(file).parse(list)

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


if __name__ == "__main__":
    main()