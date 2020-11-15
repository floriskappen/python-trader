# Example of a strategy file

class Strategy():
    HISTORY_DAYS = 30

    history = []
    flag = 0
    processing_call = False

    def __init__(self, trader):
        self.trader = trader
        pass

    def handle_new_data(self, message, exchange_id):
        # Calculate whether to buy, sell or do nothing
        pass

    def set_context_history(self, data):
        self.history.extend(data)
