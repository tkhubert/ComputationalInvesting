__author__ = 'tkhubert'

from imports import *
from Events import Events
from Market import Market

def priceCondition(t, s, prices, cutoff):
    return prices.iat[t-1,s]>=cutoff and prices.iat[t,s]<cutoff


def main():
    startD = dt.datetime(2008, 1,  1)
    endD   = dt.datetime(2009, 12, 31)

    symbolName = 'SP5002008'
    mkt = Market(startD, endD, [], symbolName)
    cutoff = 5
    events = Events(mkt, priceCondition, [mkt.d_data['actual_close'], cutoff])
    events.writeEventsResultsToFile(symbolName+'_'+str(cutoff))
    cutoff = 10
    events = Events(mkt, priceCondition, [mkt.d_data['actual_close'], cutoff])
    events.writeEventsResultsToFile(symbolName+'_'+str(cutoff))

    symbolName = 'SP5002012'
    mkt = Market(startD, endD, [], symbolName)
    cutoff = 5
    events = Events(mkt, priceCondition, [mkt.d_data['actual_close'], cutoff])
    events.writeEventsResultsToFile(symbolName+'_'+str(cutoff))
    cutoff = 10
    events = Events(mkt, priceCondition, [mkt.d_data['actual_close'], cutoff])
    events.writeEventsResultsToFile(symbolName+'_'+str(cutoff))

if __name__ == '__main__':
    main()


