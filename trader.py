import asyncio

from api.binance import Binance
from strategy.strategy import Strategy
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

        if not self.exchange.check_symbol_exists(self.symbol):
            raise SystemExit('ERROR: Symbol "{symbol}" not found on exchange "{id}"'.format(symbol=self.symbol, id=self.exchange.ID))

    def start(self):
        async def s(self):
            task = asyncio.create_task(
                self.exchange.connect_to_ticker(self.symbol, self.strategy.on_message)
            )
            await task

        asyncio.run(s(self))
