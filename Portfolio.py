__author__ = 'tkhubert'

from imports import *

class Portfolio:

    def __init__(self, dates, cash, symbols, stocksQ, prices):
        self.dates = dates
        self.cash = cash
        self.symbols = symbols
        self.stocksQ = stocksQ
        self.prices  = prices
        self.returns = prices.copy()
        tsu.returnize0(self.returns)
        self.analyzePerf()

    @classmethod
    def fromOrders(cls, mkt, orders, initialCash):
        n = len(mkt.time)
        m = len(orders.symbolSet)

        prices    = np.zeros(n)
        cash      = np.ones(n)*initialCash
        stocksQ   = np.zeros((n,m))
        mktPrices = mkt.prices[orders.symbolSet]

        orderTimes = np.searchsorted(mkt.time, orders.dates)

        for i, t in enumerate(orderTimes):
            symbol  = orders.symbols[i]
            symbIdx = orders.symbolMap[symbol]
            newQ    = stocksQ[t,symbIdx] + orders.quantity[i]
            newCash = cash[t] - orders.quantity[i]*mkt.prices[symbol][t]

            stocksQ[t:,symbIdx] = newQ
            cash[t:]            = newCash

        for t in range(n):
            prices[t] = cash[t] + np.dot(mktPrices.values[t], stocksQ[t])

        return cls(mkt.time, cash, orders.symbolSet, stocksQ, prices)


    @classmethod
    def fromMkt(cls, symbol, mkt):
        n    = mkt.prices.values.size
        return cls(mkt.time, np.zeros(n), symbol, np.zeros(n), mkt.prices.values)

    @classmethod
    def fromFile(cls, filename):
        portFile = np.loadtxt(filename, dtype='i,i,i,f', delimiter=',')

        n = portFile.size
        dates    = np.zeros(n, dtype=dt.datetime)
        prices   = np.zeros(n, dtype='f')

        i = 0
        for i, row in enumerate(portFile):
            dates[i] = dt.datetime(row[0],row[1],row[2], hour=16)
            prices[i] = row[3]
        return cls(dates, np.zeros(n), filename, np.zeros(n), prices)

    def analyzePerf(self):
        self.m  = np.mean(self.returns)
        self.s  = np.std (self.returns)
        self.sR = np.sqrt(252)*(self.m/self.s)
        self.cR = np.cumprod(1+self.returns)[-1]

    def writePricesToFile(self, filename):
        n = len(self.dates)
        y = np.zeros(n)
        m = np.zeros(n)
        d = np.zeros(n)

        for i, date in enumerate(self.dates):
            y[i] = date.year
            m[i] = date.month
            d[i] = date.day

        data = np.column_stack((y, m, d , self.prices))
        np.savetxt(filename, data, delimiter=',', fmt='%i, %i, %i, %f')

    def printPerfs(self):
        print('Final Value of Fund: ')  + str(self.prices[-1])
        print('Sharpe Ratio of Fund: '  + str(self.sR))
        print('Total Return of Fund: '  + str(self.cR))
        print('Volatility of Fund: '    + str(self.s))
        print('Average Daily Return of Fund: '  + str(self.m))
        print

    @classmethod
    def printPortPerfs(cls, port, portB):
        print('Sharpe Ratio of Fund: '  + str(port.sR))
        print('Sharpe Ratio of Bchmk: ' + str(portB.sR))
        print
        print('Total Return of Fund: '  + str(port.cR))
        print('Total Return of Bchmk: ' + str(portB.cR))
        print
        print('Volatility of Fund: '  + str(port.s))
        print('Volatility of Bchmk: ' + str(portB.s))
        print
        print('Average Daily Return of Fund: '  + str(port.m))
        print('Average Daily Return of Bchmk: ' + str(portB.m))
        print

    @classmethod
    def plotPrices(cls, portList, labels):
        plt.clf()
        dates  = portList[0].dates

        prices = portList[0].prices
        for i in range(1,len(portList)):
            prices = np.column_stack((prices, portList[i].prices))
        prices = prices / prices[0,:]

        plt.plot(dates, prices)
        plt.legend(labels)
        plt.ylabel('Adjusted Close')
        plt.xlabel('Date')
        plt.show()