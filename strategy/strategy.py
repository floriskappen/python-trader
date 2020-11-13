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

    def buy_signal(self):
        if self.flag != 1 and self.processing_call == False:
            self.processing_call = True
            success = self.trader.buy(self.history[-1])
            if success == True:
                self.processing_call = False
                self.flag = 1
            else:
                print("ERROR: Couldn't sell. Probably some logging above")

    def sell_signal(self):
        if self.flag != 0 and self.processing_call == False:
            self.processing_call = True
            success = self.trader.sell(self.history[-1])
            if success == True:
                self.processing_call = False
                self.flag = 0
            else:
                print("ERROR: Couldn't sell. Probably some logging above")

    def set_context_history(self, data):
        self.history.extend(data)
