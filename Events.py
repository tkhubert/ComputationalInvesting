__author__ = 'tkhubert'

from imports import *

class Events:

    def __init__(self, mkt, FuncCondition, args):
        self.mkt    = mkt
        self.prices = self.mkt.d_data['actual_close']
        self.events = copy.deepcopy(self.prices)*np.NAN

        nT, nS = self.prices.shape
        for t in range(1, nT):
            for s in range(nS):
                if (FuncCondition(t,s, *args)):
                    self.events.iat[t,s] = 1

    def writeEventsToOrderFile(self, quantity, filename):
        nT, nS = self.events.shape

        y = []
        m = []
        d = []
        o = []
        q = []
        symb = []

        for t in range(1, nT):
            date     = self.events.index[t]
            nextDate = self.events.index[min(t+5,nT-1)]

            for s in range(nS):
                symbol = self.events.columns[s]

                if (self.events.iat[t,s]==1):
                    y.append(date.year)
                    m.append(date.month)
                    d.append(date.day)
                    y.append(nextDate.year)
                    m.append(nextDate.month)
                    d.append(nextDate.day)
                    symb.append(symbol)
                    symb.append(symbol)
                    o.append('Buy')
                    o.append('Sell')
                    q.append(quantity)
                    q.append(quantity)

        dataType =[('y', int), ('m', int), ('d', int), ('symb', 'S5'), ('o', 'S5'), ('q', float)]
        data = np.array(zip(y, m, d, symb, o, q), dtype= dataType)
        np.savetxt(filename, data, delimiter=',', fmt='%i,%i,%i,%s,%s,%f')

    def writeEventsResultsToFile(self, filename):
        ep.eventprofiler(self.events, self.mkt.d_data, i_lookback=20, i_lookforward=20,
                s_filename=filename+'.pdf', b_market_neutral=False, b_errorbars=True)