from strategy.strategy import Strategy

class tester(Strategy):
    HISTORY_DAYS = 30

    history = []

    def handle_new_data(self, data):
        history.append(data)
        print(history)
