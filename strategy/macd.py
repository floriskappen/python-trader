import pandas
import talib
import numpy
import matplotlib.pyplot as plt

from strategy.strategy import Strategy

class Macd(Strategy):
    HISTORY_DAYS = 35

    def handle_new_data(self, data):
        self.history.append(data)
        df = pandas.DataFrame.from_dict(self.history)

        close = numpy.array(df['close'].values, dtype='f8')
        high = numpy.array(df['high'].values, dtype='f8')
        low = numpy.array(df['low'].values, dtype='f8')

        # MACD
        macd_fast_period = 12
        macd_slow_period = 26
        macd_signal_period = 9
        macd, macdsignal, macdhist = talib.MACD(
            close,
            macd_fast_period,
            macd_slow_period,
            macd_signal_period
        )
        
        # STOCH
        stoch_fask_period = 14
        stoch_slowk_period = 3
        stoch_slowk_matype = 0
        stoch_slowd_period = 3
        stoch_slowd_matype = 0
        slowk, slowd = talib.STOCH(
            high,
            low,
            close,
            fastk_period=stoch_fask_period,
            slowk_period=stoch_slowk_period,
            slowk_matype=stoch_slowk_matype,
            slowd_period=stoch_slowk_period,
            slowd_matype=stoch_slowd_matype
        )

        if macd[-1] > (macdsignal[-1] + 10):
            self.buy_signal()
        elif macd[-1] < (macdsignal[-1] - 20):
            self.sell_signal()