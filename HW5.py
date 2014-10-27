__author__ = 'tkhubert'

from imports import *
from Market import Market
from TechIndic import BollingerBands

def main():
    startD = dt.datetime(2010, 4, 1)
    endD   = dt.datetime(2010, 6, 1)
    symbol  = ['AAPL','MSFT']

    mkt = Market(startD, endD, symbol)
    BB  = BollingerBands(mkt, 20)
    #BB.plot('GOOG')
    print BB.val

if __name__=='__main__':
    main()