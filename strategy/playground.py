import pandas
from strategy.strategy import Strategy

class Playground(Strategy):
    HISTORY_DAYS = 1

    def handle_new_data(self, data):
        previous = self.history[-1]
        previousClose = float(previous['close'])
        self.history.append(data)
        close = float(data['close'])

        print(close - previousClose)
        if close > previousClose:
            return -1
        else:
            return 1

        return 0