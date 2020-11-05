import requests
import websockets

class Binance():
    ID = 'binance'
    REST_ENDPOINT = 'https://api.binance.com'
    WS_ENDPOINT = 'wss://stream.binance.com:9443/ws/'
    FEE = 0.2

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.check_status()

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
        print(response.json())
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

    def get_historical_data(self, symbol):
        params = {
            'symbol': symbol,
            'interval': '1m',
            'startTime': '1562543999999'
        }
        response = requests.get(self.REST_ENDPOINT + '/api/v3/klines', params=params)
        json = response.json()
        print(len(json))

    def check_symbol_exists(self, symbol_to_check):
        response = requests.get(self.REST_ENDPOINT + '/api/v3/exchangeInfo')
        symbols = response.json()['symbols']
        for symbol in symbols:
            if symbol['symbol'].lower() == symbol_to_check:
                return True

        return False