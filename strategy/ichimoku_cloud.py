import pandas
import numpy

from strategy.strategy import Strategy

class IchimokuCloud(Strategy):
    HISTORY_DAYS = 52

    def handle_new_data(self, data):
        self.history.append(data)
        df = pandas.DataFrame.from_dict(self.history)

        df['close'] = pandas.to_numeric(df['close'], errors = 'coerce')
        df['high'] = pandas.to_numeric(df['high'], errors = 'coerce')
        df['low'] = pandas.to_numeric(df['low'], errors = 'coerce')

        # Tenkan-sen (Conversion Line): (9-period high + 9-period low)/2))
        nine_period_high = df['high'].rolling(window = 9).max()
        nine_period_low = df['low'].rolling(window = 9).min()
        df['tenkan_sen'] = (nine_period_high + nine_period_low) /2

        # Kijun-sen (Base Line): (26-period high + 26-period low)/2))
        period26_high = df['high'].rolling(window = 26).max()
        period26_low = df['low'].rolling(window = 26).min()
        df['kijun_sen'] = (period26_high + period26_low) / 2

        # Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
        df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)

        # Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
        period52_high = df['high'].rolling(window=52).max()
        period52_low = df['low'].rolling(window=52).min()
        df['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(52)

        # The most current closing price plotted 26 time periods behind (optional)
        df['chikou_span'] = df['close'].shift(-26)

        # Above cloud
        df['above_cloud'] = 0
        df['above_cloud'] = numpy.where((df['low'] > df['senkou_span_a'])  & (df['low'] > df['senkou_span_b'] ), 1, df['above_cloud'])
        df['above_cloud'] = numpy.where((df['high'] < df['senkou_span_a']) & (df['high'] < df['senkou_span_b']), -1, df['above_cloud'])

        df['a_above_b'] = numpy.where((df['senkou_span_a'] > df['senkou_span_b']), 1, -1)

        tenkan_sen = df['tenkan_sen'].values[-1]
        kijun_sen = df['kijun_sen'].values[-1]
        senkou_span_a = df['senkou_span_a'].values[-1]
        senkou_span_b = df['senkou_span_b'].values[-1]
        chikou_span = df['chikou_span'].values[-1]
        above_cloud = df['above_cloud'].values[-1]
        a_above_b = df['a_above_b'].values[-1]
        close = df['close'].values[-1]

        # Check if we want to buy
        # if above_cloud == 1 and a_above_b == 1 and senkou_span_a > senkou_span_b and (tenkan_sen > kijun_sen or close > tenkan_sen):
        if above_cloud == 1 and a_above_b == 1:
            return 1
        # Check if we want to sell
        # elif above_cloud == -1 and a_above_b == -1 and senkou_span_a < senkou_span_b and (tenkan_sen < kijun_sen or close < tenkan_sen):
        elif above_cloud == -1 and a_above_b == -1:
            return -1

        return 0