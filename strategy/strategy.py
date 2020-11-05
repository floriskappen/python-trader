# Example of a strategy file

class Strategy():
    def __init__(self, trader):
        self.trader = trader
        pass

    def on_message(self, message, exchange_id):
        # Calculate whether to buy, sell or do nothing
        pass

    def buy_signal(self):
        # self.trader.buy()
        pass

    def sell_signal(self):
        # self.trader.sell()
        pass
