# Example of a strategy file

class Strategy():
    HISTORY_DAYS = 30

    history = []

    def __init__(self, trader):
        self.trader = trader
        pass

    def handle_new_data(self, message, exchange_id):
        # Calculate whether to buy, sell or do nothing
        pass

    def buy_signal(self):
        # self.trader.buy()
        pass

    def sell_signal(self):
        # self.trader.sell()
        pass

    def set_context_history(self, data):
        self.history.append(data)
