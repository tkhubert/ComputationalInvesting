__author__ = 'tkhubert'

from imports import *
from Market import Market

class BollingerBands:

    def __init__(self, mkt, period):
        self.mkt = mkt
        self.period = period
        self.computeBands()

    def computeBands(self):
        self.prices = self.mkt.prices
        self.means = pd.rolling_mean(self.prices, self.period)
        self.stds  = pd.rolling_std (self.prices, self.period)
        self.up    = self.means + self.stds
        self.dwn   = self.means - self.stds
        self.val   = (self.prices-self.means)/self.stds

    def indicator(self, t, s, sBench):
        return (self.val.iat[t-1,s]>=-2 and self.val.iat[t,s]<=-2 and self.val.iat[t,sBench]>=1)

    def plot(self, symbolName):
        p = self.prices[symbolName].values
        m = self.means[symbolName].values
        u = self.up[symbolName].values
        d = self.dwn[symbolName].values
        t = self.mkt.prices.index

        legend = ['p','m','u','d']

        plt.clf()
        plt.plot(t, p)
        plt.plot(t, m)
        plt.plot(t, u)
        plt.plot(t, d)
        plt.legend(legend)
        plt.ylabel('Adjusted Close')
        plt.xlabel('Date')
        plt.show()