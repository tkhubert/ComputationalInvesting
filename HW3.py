__author__ = 'tkhubert'

from Orders    import Orders
from Market    import Market
from Portfolio import Portfolio

def main():
    inputFile   = 'orders2.csv'
    outputFile  = 'orders2.out.csv'
    benchmark   = ['$SPX']
    initialCash = 1000000

    orders = Orders(inputFile)
    mkt    = Market(orders.dates[0], orders.dates[-1], orders.symbolSet)
    mktB   = Market(orders.dates[0], orders.dates[-1], benchmark)
    port   = Portfolio.fromOrders(mkt, orders, initialCash)
    portB  = Portfolio.fromMkt(benchmark, mktB)
    Portfolio.printPortPerfs(port, portB)
    port.writePricesToFile(outputFile)

    #portT  = Portfolio.fromFile(outputFile)
    #printPortPerf(port, portT)
    Portfolio.plotPrices([port, portB], ['port', 'benchmark'])

if __name__ == '__main__':
    main()