import asyncio
import pandas
import matplotlib.pyplot as plt
import talib
import numpy
import datetime
import atexit

from api.binance import Binance
from reporter import Reporter

# Strategies
from strategy.playground import Playground
from strategy.macd_stochastic import MacdStochastic
from strategy.macd import Macd

import helpers

class Trader():
    EXCHANGES = {
        'binance': Binance
    }
    STRATEGIES = {
        'playground': Playground,
        'macd_stochastic': MacdStochastic,
        'macd': Macd,
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

        self.type = config['type']
        if self.type == 'live':
            self.paper_trade = config['paper_trade']

        if not self.exchange.check_symbol_exists(self.symbol):
            raise SystemExit('ERROR: Symbol "{symbol}" not found on exchange "{id}"'.format(symbol=self.symbol, id=self.exchange.ID))

    # def start(self):


    def live_trade(self):
        # TODO: Check if user has enough funds in account if not paper trading
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
        self.strategy.set_context_history(context_historical_data)

        async def start(self):
            task = asyncio.create_task(
                self.exchange.connect_to_kline(self.symbol, self.interval, self.strategy.handle_new_data)
            )
            await task

        atexit.register(self.reporter.create_report, self.strategy.history)

        asyncio.run(start(self))


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
        if self.type == 'backtest':
            self.reporter.register_buy_reference(reference)
        elif self.type == 'live':
            if self.paper_trade == True:
                self.reporter.register_buy_reference(reference)
            elif self.paper_trade == False:
                # TODO: Send buy request to exchance. If succesfull, continue
                self.reporter.register_buy_reference(reference)

    def sell(self, reference):
        if self.type == 'backtest':
            self.reporter.register_sell_reference(reference)
        elif self.type == 'live':
            if self.paper_trade == True:
                self.reporter.register_sell_reference(reference)
            elif self.paper_trade == False:
                # TODO: Send buy request to exchance. If succesfull, continue
                self.reporter.register_sell_reference(reference)

