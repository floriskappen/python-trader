import asyncio
import pandas
import matplotlib.pyplot as plt
import talib
import numpy
import datetime

from api.binance import Binance
from strategy.strategy import Strategy
import helpers

class Trader():
    EXCHANGES = {
        'binance': Binance
    }
    STRATEGIES = {
        'strategy': Strategy
    }

    def __init__(self, config, secrets):
        self.strategy = self.STRATEGIES[config['strategy']](self)
        self.exchange = self.EXCHANGES[config['exchange']](
            secrets['keys'][config['exchange']]['key'],
            secrets['keys'][config['exchange']]['secret']
        )
        self.symbol = config['symbol'].lower()
        self.interval = config['interval']

        if not self.exchange.check_symbol_exists(self.symbol):
            raise SystemExit('ERROR: Symbol "{symbol}" not found on exchange "{id}"'.format(symbol=self.symbol, id=self.exchange.ID))

    # def start(self):
    #     async def s(self):
    #         task = asyncio.create_task(
    #             self.exchange.connect_to_ticker(self.symbol, self.strategy.on_message)
    #         )
    #         await task

    #     asyncio.run(s(self))

    def live_trade(self):
        # Get history so strategy has enough context
        history_days = self.strategy.HISTORY_DAYS
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=history_days)
        history_days_ago = now - delta
        period = {
            'start': int(history_days_ago.timestamp() * 1000),
            'end': int(now.timestamp() * 1000)
        }
        context_historical_data = self.exchange.get_historical_data(
                                                                symbol=self.symbol.upper(),
                                                                interval=self.interval,
                                                                period=period
                                                            )
        print(context_historical_data)


    def backtest(self, period):
        history_days = self.strategy.HISTORY_DAYS
        start_datetime = datetime.datetime.fromtimestamp(period['start'])
        delta = datetime.timedelta(days=history_days)
        history_days_ago = start_datetime - delta
        context_period = {
            'start': int(history_days_ago.timestamp() * 1000),
            'end': int(start_datetime.timestamp() * 1000)
        }

        context_historical_data = self.exchange.get_historical_data(
                                                                        symbol=self.symbol.upper(),
                                                                        interval=self.interval,
                                                                        period=context_period
                                                                    )

        self.strategy.set_context_history(context_historical_data)

        historical_data = self.exchange.get_historical_data(
                                                                symbol=self.symbol.upper(),
                                                                interval=self.interval,
                                                                period=period
                                                            )

        # Send data to strategy
        for data in historical_data:
            self.strategy.handle_new_data(data)


        # Everything underneath here should be moved to a strategy somehow
        # print(historical_data)
        df = pandas.DataFrame.from_dict(historical_data)
        df.set_index(pandas.DatetimeIndex(df['date'].values))

        period = 20

        # MACD
        df['np_close'] = numpy.array(df['close'], dtype='float')
        df['np_high'] = numpy.array(df['high'], dtype='float')
        df['np_low'] = numpy.array(df['low'], dtype='float')
        df['macd'], df['macdsignal'], macdhist = talib.MACD(df['np_close'], fastperiod=12, slowperiod=26, signalperiod=9)
        df['slowk'], df['slowd'] = talib.STOCH(df['np_high'], df['np_low'], df['np_close'], fastk_period=5, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
        # Buy sell
        money = 1500
        buys = 0
        sells = 0
        flag = -1
        for i in range(len(df['macd'])):
            if df['macd'][i] > df['macdsignal'][i]:
                if flag != 1:
                    money -= int(float(df['close'][i]))
                    buys += 1
                    flag = 1
            elif df['macd'][i] < df['macdsignal'][i]:
                if flag != 0:
                    money += int(float(df['close'][i]))
                    sells += 1
                    flag = 0

        if flag == 1:
            money += int(float(df['close'].values[-1]))

        print(money)
        print(buys)
        print(sells)

        
        plt.figure(figsize=(20, 4.5))
        plt.plot(df['macd'], label = 'BTC MACD', color = 'red')
        plt.plot(df['macdsignal'], label = 'Signal Line', color = 'blue')
        # plt.plot(df['slowk'], label = 'slowk', color = 'orange')
        # plt.plot(df['slowd'], label = 'slowd', color = 'green')
        plt.legend(loc = 'upper left')
        plt.show()

    def on_buy_signal(self):
        print('Buying')
