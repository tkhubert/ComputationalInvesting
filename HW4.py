__author__ = 'tkhubert'

from imports import *
from Events import Events
from Market import Market
from Orders import Orders

from Portfolio import Portfolio

def priceCondition(t, s, prices, cutoff):
    return prices.iat[t-1,s]>=cutoff and prices.iat[t,s]<cutoff

def main():
    startD = dt.datetime(2008, 1,  1)
    endD   = dt.datetime(2009, 12, 31)

    symbolName  = 'SP5002012'
    benchmark   = ['$SPX']
    cutoff      = 5
    quantity    = 100
    initialCash = 50000
    orderFileName = 'ordersFromEvent.csv'

    mkt  = Market(startD, endD, [], symbolName)
    mktB = Market(startD, endD, benchmark)

    events = Events(mkt, priceCondition, [mkt.d_data['actual_close'], cutoff])
    events.writeEventsToOrderFile(quantity, orderFileName)
    orders = Orders(orderFileName)

    port  = Portfolio.fromOrders(mkt, orders, initialCash)
    portB = Portfolio.fromMkt(benchmark, mktB)

    port.printPerfs()
    Portfolio.printPortPerfs(port, portB)
    Portfolio.plotPrices([port, portB], ['port', 'benchmark'])

if __name__ == '__main__':
    main()