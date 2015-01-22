__author__ = 'claesma1'


class CurrentAssets( ):
    def __init__(self):
        self.Cash = ""
        self.AccountsReceivable = ""
        self.PrepaidExpenses = ""
        self.ForeignSalesTaxReceivable = ""
        self.DeferredIncomeTaxes = ""
        self.Other = ""
        self.AssetsDiscontinuedOperations = ""
        self.Total = ""

class Assets( ):
    def __init__(self):
        self.CurrentAssets = CurrentAssets()

class Liabilities( ):
    def __init__(self):
        self.CurrentLiabilities = ""

class Balance( ):
    def __init__(self):
        self.Assets = Assets()
        self.Liabilities = Liabilities()

class OperatingCosts( ):
    def __init__(self):
        self.Sales = ""
        self.RD = ""
        self.General = ""
        self.Amortization = ""
        self.Total = ""

class Operations( ):
    def __init__(self):
        self.Revenue = ""
        self.CostGoodsSold = ""
        self.OperatingCosts = OperatingCosts()

class Info( ):
    def __init__(self):
        self.Year = ""
        self.Employees = ""

class AnnualReport( ):
    def __init__(self):
        self.Info = Info()
        self.Balance = Balance()
        self.Operations = Operations()

