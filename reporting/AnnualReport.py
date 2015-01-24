__author__ = 'claesma1'


class Assets():
    def __init__(self):
        self.CurrentAssets = \
            {'Cash': 0, 'AccountsReceivable': 0, 'PrepaidExpenses': 0,
             'ForeignSalesTaxReceivable': 0, 'DeferredIncomeTaxes': 0,
             'Other': 0, 'AssetsDiscontinuedOperations': 0, 'Total': 0}

class Liabilities():
    def __init__(self):
        self.CurrentLiabilities = ""

class Balance():
    def __init__(self):
        self.Assets = Assets()
        self.Liabilities = Liabilities()

class Operations():
    def __init__(self):
        self.Revenue = ""
        self.CostGoodsSold = ""
        self.NetIncome = ""
        self.OperatingCosts = \
            {'Sales': 0, 'RD': 0, 'General': 0, 'Amortization': 0, 'Total': 0}

class AnnualReport():
    def __init__(self):
        self.Info = {'Year': 0, 'Employees': 0, }
        self.Balance = Balance()
        self.Operations = Operations()

