import asyncio
import pandas
import matplotlib.pyplot as plt
import talib
import numpy
import datetime

from api.binance import Binance
from reporter import Reporter
from strategy.strategy import Strategy
from strategy.tester import Tester
import helpers

class Trader():
    EXCHANGES = {
        'binance': Binance
    }
    STRATEGIES = {
        'strategy': Strategy,
        'tester': Tester
    }

    def __init__(self, config, secrets):
        self.strategy = self.STRATEGIES[config['strategy']](self)
        self.exchange = self.EXCHANGES[config['exchange']](
            secrets['keys'][config['exchange']]['key'],
            secrets['keys'][config['exchange']]['secret']
        )
        self.symbol = config['symbol'].lower()
        self.interval = config['interval']
        self.reporter = Reporter(config['starting_amount'], self.exchange.FEE)

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
        timestamp = period['start']
        start_datetime = datetime.datetime.fromtimestamp(timestamp / 1000)
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

        # Sell leftover
        self.strategy.sell_signal()

        self.reporter.create_report(self.strategy.history)

    def buy(self, reference):
        self.reporter.register_buy_reference(reference)

    def sell(self, reference):
        self.reporter.register_sell_reference(reference)
