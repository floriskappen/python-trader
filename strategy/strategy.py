# Example of a strategy file

class Strategy():
    HISTORY_DAYS = 30

    history = []
    flag = 0

    def __init__(self, trader):
        self.trader = trader
        pass

    def handle_new_data(self, message, exchange_id):
        # Calculate whether to buy, sell or do nothing
        pass

    def buy_signal(self):
        if self.flag != 1:
            self.trader.buy(self.history[-1])
            self.flag = 1

    def sell_signal(self):
        if self.flag != 0:
            self.trader.sell(self.history[-1])
            self.flag = 0

    def set_context_history(self, data):
        self.history.extend(data)
