__author__ = 'tkhubert'

from imports import *
from TechIndic import BollingerBands
from Events import Events
from Market import Market


def main():
    startD = dt.datetime(2008, 1 , 1)
    endD   = dt.datetime(2009, 12, 31)
    symbolList = 'SP5002012'
    benchmark  = ['SPY']

    mkt = Market(startD, endD, benchmark, symbolList)
    BB  = BollingerBands(mkt, 20)
    sBenchmark = len(mkt.prices.columns) -1
    events = Events(mkt, BB.indicator, [sBenchmark])
    events.writeEventsResultsToFile('testEvent')

if __name__=='__main__':
    main()