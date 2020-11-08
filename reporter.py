import matplotlib.pyplot as plt
import pandas
import numpy

class Reporter():
    buy_references = []
    sell_references = []
    amount = 0
    funds = 0

    def __init__(self, funds, fee):
        self.funds = funds
        self.fee = fee

    def register_buy_reference(self, reference):
        self.buy_references.append(reference)
        close = reference['close']
        self.amount = self.funds / float(close)
        tax = (self.amount / 100) * self.fee
        self.amount -= tax
        
        self.funds = 0


    def register_sell_reference(self, reference):
        self.sell_references.append(reference)
        close = reference['close']
        self.funds = self.amount * float(close)
        tax = (self.funds / 100) * self.fee
        self.funds -= tax
        self.amount = 0

    def create_report(self, history):
        padded_buy_references = []
        padded_sell_references = []

        for reference in history:
            appended_buy_reference = False
            appended_sell_reference = False
            for buy_reference in self.buy_references:
                if buy_reference['open_time'] == reference['open_time']:
                    padded_buy_references.append(reference['close'])
                    appended_buy_reference = True
            if not appended_buy_reference:
                padded_buy_references.append(numpy.nan)

            for sell_reference in self.sell_references:
                if sell_reference['open_time'] == reference['open_time']:
                    padded_sell_references.append(reference['close'])
                    appended_sell_reference = True
            if not appended_sell_reference:
                padded_sell_references.append(numpy.nan)


        df = pandas.DataFrame.from_dict(history)
        df['buy_signals'] = padded_buy_references
        df['sell_signals'] = padded_sell_references
        close = numpy.array(df['close'].values, dtype='f8')

        plt.figure(figsize=(16, 4.5))
        plt.plot(
            close,
            label = 'Closing Price',
            color = 'black',
            alpha = 0.3
        )
        print('AMOUNT: ' + str(self.amount))
        print('FUNDS: ' + str(self.funds))
        print('Total Trades: ' + str(len(self.buy_references) + len(self.sell_references)))
        print('Buy Trades: ' + str(len(self.buy_references)))
        print('Sell Trades: ' + str(len(self.sell_references)))
        plt.scatter(df.index, df['buy_signals'].values, color = 'green', label = 'Buy', marker = '^')
        plt.scatter(df.index, df['sell_signals'].values, color = 'red', label = 'Sell', marker = 'v')
        plt.show()