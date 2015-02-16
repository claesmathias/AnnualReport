__author__ = 'claesmathias'

import xml.etree.ElementTree as ET
from Utilities import Utilities
from Reporting import *

class XMLParser():

    def __init__(self, file):
        self.file = file

    def parse(self, list, function_filter):
        # Parse the given file
        tree = ET.parse(self.file)

        # Get the XML root
        root = tree.getroot()

        # Find the 'Report' tag
        for report in root.findall('Report'):
            # Find the info element
            info = report.find('Info')

            # Check the type
            if info.find('Type').text == "10-K":
                # Create a new annual report
                r = AnnualReport()
            elif info.find('Type').text == "10-Q":
                # Create a new quarterly earnings
                r = QuarterlyEarnings()

            #
            # Parse the info statement, Iterate over keys and set values
            i = r.Info
            Utilities.set_dictionary_xml(i, info)

            #
            # Parse the Consolidated Statements of Operations Data
            operations = report.find('Operations')
            o = r.Operations
            o.Revenue = operations.find('Revenue').text
            o.CostGoodsSold = operations.find('CostGoodsSold').text
            o.ProvisionIncomeTaxes = operations.find('ProvisionIncomeTaxes').text
            o.NetIncome = operations.find('NetIncome').text

            # Parse the operating costs
            operating_cost = operations.find('OperatingCosts')
            oc = r.Operations.OperatingCosts
            # Iterate over keys and set values
            Utilities.set_dictionary_xml(oc, operating_cost)

            # Parse the operating income
            operating_income = operations.find('OperatingIncome')
            oi = r.Operations.OperatingIncome
            # Iterate over keys and set values
            Utilities.set_dictionary_xml(oi, operating_income)

            # For now only parse the Balance sheet for annual reports
            if isinstance(r, AnnualReport):
                #
                # Parse the Consolidated Balance Sheets
                balance = report.find('Balance')

                # Parse the assets
                assets = balance.find('Assets')
                a = r.Balance.Assets
                a.Total = assets.find('Total').text
                # Parse the current assets
                current_assets = assets.find('CurrentAssets')
                ca = a.CurrentAssets
                # Iterate over keys and set values
                Utilities.set_dictionary_xml(ca, current_assets)

                # Parse the liabilities
                liabilities = balance.find('Liabilities')
                l = r.Balance.Liabilities
                # Parse the current assets
                current_liabilities = liabilities.find('CurrentLiabilities')
                cl = l.CurrentLiabilities
                # Iterate over keys and set values
                Utilities.set_dictionary_xml(cl, current_liabilities)
                # Parse other
                l.StockholderEquity = liabilities.find('StockholderEquity').text

            # Add the new annual report to the list
            list.append(r)

            # Filter the list
            list = filter(function_filter, list)