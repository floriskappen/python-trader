from strategy.strategy import Strategy

class Playground(Strategy):
    HISTORY_DAYS = 10

    def handle_new_data(self, data):
        previous = self.history[-1]
        self.history.append(data)
        if data['open'] > previous['open']:
            self.sell_signal()
        else:
            self.buy_signal()