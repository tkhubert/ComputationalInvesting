__author__ = 'tkhubert'

from imports import *

class Market:

    def __init__(self, startD, endD, symbols, symbolsListName=None):

        self.startD  = startD
        self.endD    = endD

        dataAccess = da.DataAccess('Yahoo')#,  cachestalltime=0)

        toD  = dt.timedelta(hours=16)
        self.time = du.getNYSEdays(startD, endD, toD)

        keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

        if (symbolsListName!=None):
            symbolsList = dataAccess.get_symbols_from_list(symbolsListName)
            self.symbols = symbolsList + symbols
        else:
            self.symbols = symbols

        df_data = dataAccess.get_data(self.time, self.symbols, keys)
        self.d_data  = dict(zip(keys, df_data))

        for key in keys:
            self.d_data[key] = self.d_data[key].fillna(method='ffill')
            self.d_data[key] = self.d_data[key].fillna(method='bfill')
            self.d_data[key] = self.d_data[key].fillna(1.0)

        self.prices = self.d_data['close']