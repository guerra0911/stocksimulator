import datetime
from stocks import getPrice

###PORTFOLIO###
def modifyPortfolio(user, type, numShares, stock):
    if type == "Buy":
        #If Stock exists, then don't append the stock, just add the numShares and price data
        pass
    else:
        #Remove Stock from Stock list, only according to # of shares and if they don't own them
        pass

    price = getPrice(stock)
    date = datetime.datetime.now()
    #Append -> Type, # SHARES, Stock, Price, Date to Portfolio Table for user
    pass

def addToStockList(user):
    pass

def getStockList(user):
    #Return a list of all the stocks a user owns, and how much money in each
    pass

def getTransactions(user):
    #Return a list of all the transactions a user made
    pass