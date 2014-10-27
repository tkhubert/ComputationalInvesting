__author__ = 'tkhubert'

from imports import *
from TechIndic import BollingerBands
from Events import Events
from Market import Market
from Orders import Orders
from Portfolio import Portfolio

def main():
    startD = dt.datetime(2008, 1 , 1)
    endD   = dt.datetime(2009, 12, 31)
    symbolList = 'SP5002012'
    benchmark  = ['SPY']
    quantity   = 100
    orderFileName = 'orderBB.csv'
    intialCash = 100000

    mkt = Market(startD, endD, benchmark, symbolList)
    mktB = Market(startD, endD, benchmark)

    BB  = BollingerBands(mkt, 20)
    sBenchmark = len(mkt.prices.columns) -1
    events = Events(mkt, BB.indicator, [sBenchmark])
    events.writeEventsResultsToFile('testEvent')
    events.writeEventsToOrderFile(quantity, orderFileName)
    orders = Orders(orderFileName)

    port  = Portfolio.fromOrders(mkt, orders, intialCash)
    portB = Portfolio.fromMkt(benchmark, mktB)

    port.printPerfs()
    Portfolio.printPortPerfs(port, portB)
    Portfolio.plotPrices([port, portB], ['port', 'benchmark'])

if __name__=='__main__':
    main()