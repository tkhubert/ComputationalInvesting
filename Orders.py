__author__ = 'tkhubert'

from imports import *

class Orders:

    def __init__(self, orderFileName):
        dataType =[('y', int), ('m', int), ('d', int), ('symb', 'S5'), ('o', 'S5'), ('q', float)]
        ordersFile = np.loadtxt(orderFileName, dtype=dataType, delimiter=',')

        n = ordersFile.size
        dates    = np.zeros(n, dtype=dt.datetime)
        symbols  = np.empty(n, dtype='S10')
        quantity = np.zeros(n)

        i = 0
        for order in ordersFile:
            dates   [i] = dt.datetime(order[0],order[1],order[2], hour=16)
            symbols [i] = order[3]
            quantity[i] = (2*(order[4]=='Buy')-1)*order[5]
            i +=1

        idxs = dates.argsort()
        self.size  = n
        self.dates = dates[idxs]
        self.symbols = symbols[idxs]
        self.quantity = quantity[idxs]

        self.symbolSet = np.unique(symbols)
        self.symbolMap = dict(zip(self.symbolSet, range(0,len(self.symbolSet))))
