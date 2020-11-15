import pandas
import talib
import numpy

from strategy.strategy import Strategy

class BollingerBands(Strategy):
    HISTORY_DAYS = 52

    def handle_new_data(self, data):
        self.history.append(data)
        df = pandas.DataFrame.from_dict(self.history)

        df['close'] = pandas.to_numeric(df['close'], errors = 'coerce')
        close = numpy.array(df['close'].values, dtype='f8')

        upper, middle, lower = talib.BBANDS(close, matype=talib.MA_Type.T3)

        # Check if we want to buy
        if close[-1] < lower[-1]:
            return 1
        # Check if we want to sell
        if close[-1] > upper[-1]:
            return -1

        return 0