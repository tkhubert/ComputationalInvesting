__author__ = 'tkhubert'

from imports import *

def getPrices(startD, endD, symbols):

    dataAccess = da.DataAccess('Yahoo',  cachestalltime=0)

    toD  = dt.timedelta(hours=16)
    time = du.getNYSEdays(startD, endD, toD)

    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    df_data = dataAccess.get_data(time, symbols, keys)
    d_data  = dict(zip(keys, df_data))

    for key in keys:
        d_data[key] = d_data[key].fillna(method='ffill')
        d_data[key] = d_data[key].fillna(method='bfill')
        d_data[key] = d_data[key].fillna(1.0)

    prices = d_data['close'].values
    prices = prices / prices[0,:]

    return prices

def simulate(prices, alloc):

    portPrice = np.sum(prices * alloc, axis=1)
    portReturn = portPrice.copy()
    tsu.returnize0(portReturn)

    m  = np.mean(portReturn)
    s  = np.std(portReturn)
    sR = np.sqrt(252)*(m/s)
    cR = np.cumprod(1+portReturn)[-1]

    return [m,s,sR,cR]

def bruteForceOptimize(startD, endD, symbols):

    prices = getPrices(startD, endD, symbols)
    alloc     = [0., 0., 0., 0.]
    bestAlloc = [1., 0., 0., 0.]
    bestSR    = simulate(prices,bestAlloc)[2]

    for w0 in range(0,11):
        alloc[0]=w0/10.
        for w1 in range(0,11):
            alloc[1]=w1/10.
            if (w0+w1>10):
                break
            for w2 in range(0,11):
                alloc[2]=w2/10.
                if (w0+w1+w2>10):
                    break
                for w3 in range(0,11):
                    alloc[3]=w3/10.
                    if (w0+w1+w2+w3!=10):
                        continue
                    res = simulate(prices,alloc)
                    sR = res[2]
                    if (sR>bestSR):
                        bestSR = sR
                        bestAlloc = [w0/10., w1/10., w2/10., w3/10.]

    return [bestSR, bestAlloc]

def printSimResults(results):
    print('Sharpe Ratio: ' + str(results[2]))
    print('Volatility (stdev of daily returns): ' + str(results[1]))
    print('Average Daily Return: ' + str(results[0]))
    print('Cumulative Return: ' + str(results[3]))
    print

def printOptResults(results):
    print('Best Sharpe Ratio: ' + str(results[0]))
    print('Best Allocation: ' + str(results[1]))
    print

def plotOptResults(startD, endD, symbols):
    toD  = dt.timedelta(hours=16)
    time = du.getNYSEdays(startD, endD, toD)

    res = bruteForceOptimize(startD, endD, symbols)

    prices = getPrices(startD, endD, symbols)
    portPrice = np.sum(prices * res[1], axis=1)
    allPrice = np.column_stack((prices, portPrice))
    legend  = symbols + ['port']

    plt.clf()
    plt.plot(time, allPrice)
    plt.legend(legend)
    plt.ylabel('Adjusted Close')
    plt.xlabel('Date')
    plt.show()


def main():
    # startD  = dt.datetime(2011,1 ,1 )
    # endD    = dt.datetime(2011,12,31)
    # symbols = ['AAPL', 'GLD', 'GOOG', 'XOM']
    # alloc   = [0.4, 0.4, 0.0, 0.2]
    # prices = getPrices(startD, endD, symbols)
    # res = simulate(prices, alloc)
    # printSimResults(res)
    #
    # startD  = dt.datetime(2010,1 ,1 )
    # endD    = dt.datetime(2010,12,31)
    # symbols = ['AXP', 'HPQ', 'IBM', 'HNZ']
    # alloc   = [0.0, 0.0, 0.0, 1.0]
    # prices = getPrices(startD, endD, symbols)
    # res = simulate(prices, alloc)
    # printSimResults(res)

    # startD  = dt.datetime(2011,1 ,1 )
    # endD    = dt.datetime(2011,12,31)
    # symbols = ['BRCM', 'TXN', 'AMD', 'ADI']
    # prices = getPrices(startD, endD, symbols)
    # res  = bruteForceOptimize(startD, endD, symbols)
    # res2 = simulate(prices, res[1])
    # printSimResults(res2)
    # printOptResults(res)
    #
    # startD  = dt.datetime(2011,1 ,1 )
    # endD    = dt.datetime(2011,12,31)
    # symbols = ['C', 'GS', 'IBM', 'HNZ']
    # prices = getPrices(startD, endD, symbols)
    # res = bruteForceOptimize(startD, endD, symbols)
    # res2 = simulate(prices, res[1])
    # printSimResults(res2)
    # printOptResults(res)

    startD  = dt.datetime(2011,1 ,1 )
    endD    = dt.datetime(2011,12,31)
    symbols = ['GOOG', 'AAPL', 'IBM', 'GLD']
    prices = getPrices(startD, endD, symbols)
    res = bruteForceOptimize(startD, endD, symbols)
    res2 = simulate(prices, res[1])
    printSimResults(res2)
    printOptResults(res)
    plotOptResults(startD, endD, symbols)

if __name__ == '__main__':
    main()


