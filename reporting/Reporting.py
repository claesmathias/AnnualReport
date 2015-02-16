__author__ = 'claesmathias'


class Assets():
    def __init__(self):
        self.CurrentAssets = \
            {'Cash': 0, 'AccountsReceivable': 0, 'Inventories': 0, 'PrepaidExpenses': 0,
             'ForeignSalesTaxReceivable': 0, 'DeferredIncomeTaxes': 0,
             'Other': 0, 'AssetsDiscontinuedOperations': 0, 'Total': 0}
        self.Total = ""

class Liabilities():
    def __init__(self):
        self.CurrentLiabilities = \
            {'AccountsPayable': 0, 'DeferredRevenue': 0, 'AccruedWagesPayrollTaxes': 0,
             'IncomeTaxesPayable': 0,'OtherAccruedExpenses': 0, 'DeferredCompensation': 0,
             'LiabilitiesDiscontinuedOperations': 0, 'Total': 0}
        self.StockholderEquity = ""

class Balance():
    def __init__(self):
        self.Assets = Assets()
        self.Liabilities = Liabilities()

class Operations():
    def __init__(self):
        self.Revenue = ""
        self.CostGoodsSold = ""
        self.NetIncome = ""
        self.ProvisionIncomeTaxes = ""
        self.OperatingCosts = \
            {'Sales': 0, 'RD': 0, 'General': 0, 'Amortization': 0, 'Total': 0}
        self.OperatingIncome = \
            {'OperatingIncome': 0, 'InterestIncome': 0, 'OtherIncome': 0, 'Total': 0}

class AnnualReport():
    def __init__(self):
        self.Info = {'Type': "", 'Year': 0, 'Employees': 0, 'Company': ""}
        self.Balance = Balance()
        self.Operations = Operations()

class QuarterlyEarnings():
    def __init__(self):
        self.Info = {'Type': "", 'Quarter': "", 'Year': 0, 'Company': ""}
        self.Balance = Balance()
        self.Operations = Operations()