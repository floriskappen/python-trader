import requests
import websockets
import datetime
import time

from api.exchange import Exchange

class Binance(Exchange):
    ID = 'binance'
    REST_ENDPOINT = 'https://api.binance.com'
    WS_ENDPOINT = 'wss://stream.binance.com:9443/ws/'
    FEE = 0.1

    def check_status(self):
        wallet_up = self.check_wallet_status()
        server_up = self.check_rest_status()

    def check_wallet_status(self):
        response = requests.get(self.REST_ENDPOINT + '/wapi/v3/systemStatus.html')
        if response.status_code == 200:
            status = response.json()
            if status == 0:
                return True
        return False
    
    def check_rest_status(self):
        response = requests.get(self.REST_ENDPOINT + '/api/v3/time')
        if response.status_code == 200:
            return True
        return False

    async def connect_to_ticker(self, symbol, on_message):
        uri = self.WS_ENDPOINT + symbol + '@miniTicker@1000ms'
        ws = await websockets.connect(uri)

        print('START: Connected to ticket "{id}" for symbol "{symbol}"'.format(id=self.ID, symbol=symbol))

        try:
            while True:
                msg = await ws.recv()
                on_message(msg, self.ID)
        except websockets.WebSocketException as wse:
            print(wse)
            pass

    def get_historical_data(self, symbol, interval, period):
        start = period['start']
        data = []
        while start < period['end']:
            params = {
                'symbol': symbol,
                'interval': interval,
                'startTime': start
            }
            response = requests.get(self.REST_ENDPOINT + '/api/v3/klines', params=params)
            parsed_response = response.json()
            last_entry = parsed_response[-1]
            data.extend(parsed_response)
            start = last_entry[0] + 1

        # Convert to dictionary
        parsed_data = []
        for element in data:
            date = datetime.datetime.fromtimestamp(element[0] / 1000.0).strftime('%Y-%m-%d %H:%M:%S.%f')
            parsed_data.append({
                'open_time': element[0],
                'close_time': element[5],
                'open': element[1],
                'close': element[4],
                'high': element[2],
                'low': element[3],
                'number_of_trades': element[7],
                'date': date
            })

        return parsed_data

    def get_time_difference(self):
        response = requests.get(self.REST_ENDPOINT + '/api/v3/time')
        local_time = datetime.datetime.now().timestamp() * 1000
        server_time = response.json()['serverTime']
        return server_time - local_time

    def check_symbol_exists(self, symbol_to_check):
        response = requests.get(self.REST_ENDPOINT + '/api/v3/exchangeInfo')
        symbols = response.json()['symbols']
        for symbol in symbols:
            if symbol['symbol'].lower() == symbol_to_check:
                return True

        return False