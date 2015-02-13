__author__ = 'claesmathias'

import xml.etree.ElementTree as ET
from Utilities import Utilities
from AnnualReport import AnnualReport

class XMLParser():

    def __init__(self, file):
        self.file = file

    def parse(self, list):
        # Parse the given file
        tree = ET.parse(self.file)

        # Get the XML root
        root = tree.getroot()

        # Find the 'Report' tag
        for report in root.findall('Report'):
            # Create a new annual report
            ar = AnnualReport()

            #
            # Parse the info statement, Iterate over keys and set values
            info = report.find('Info')
            i = ar.Info
            Utilities.set_dictionary_xml(i, info)

            #
            # Parse the Consolidated Statements of Operations Data
            operations = report.find('Operations')
            o = ar.Operations
            o.Revenue = operations.find('Revenue').text
            o.CostGoodsSold = operations.find('CostGoodsSold').text
            o.ProvisionIncomeTaxes = operations.find('ProvisionIncomeTaxes').text
            o.NetIncome = operations.find('NetIncome').text

            # Parse the operating costs
            operating_cost = operations.find('OperatingCosts')
            oc = ar.Operations.OperatingCosts
            # Iterate over keys and set values
            Utilities.set_dictionary_xml(oc, operating_cost)

            # Parse the operating income
            operating_income = operations.find('OperatingIncome')
            oi = ar.Operations.OperatingIncome
            # Iterate over keys and set values
            Utilities.set_dictionary_xml(oi, operating_income)

            #
            # Parse the Consolidated Balance Sheets
            balance = report.find('Balance')

            # Parse the assets
            assets = balance.find('Assets')
            a = ar.Balance.Assets
            a.Total = assets.find('Total').text
            # Parse the current assets
            current_assets = assets.find('CurrentAssets')
            ca = a.CurrentAssets
            # Iterate over keys and set values
            Utilities.set_dictionary_xml(ca, current_assets)

            # Parse the liabilities
            liabilities = balance.find('Liabilities')
            l = ar.Balance.Liabilities
            # Parse the current assets
            current_liabilities = liabilities.find('CurrentLiabilities')
            cl = l.CurrentLiabilities
            # Iterate over keys and set values
            Utilities.set_dictionary_xml(cl, current_liabilities)
            # Parse other
            l.StockholderEquity = liabilities.find('StockholderEquity').text


            # Add the new annual report to the list
            list.append(ar)