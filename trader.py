class Trader():
    def __init__(self, strategy, exchange, url):
        self.strategy = strategy
        self.exchange = exchange
        self.url = url
        pass

    def start(self):
        # Make this asyncio
        # self.exchange.connect_to_ticker(self.url, self.strategy.on_message())
