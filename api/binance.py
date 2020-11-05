import requests
import asyncio
import websockets

class Binance():
    ID = 'binance'
    REST_ENDPOINT = 'https://api.binance.com'
    WS_ENDPOINT = 'wss://stream.binance.com:9443'
    FEE = 0.2

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.check_status()

    def check_status(self):
        wallet_up = self.check_wallet_status()

    def check_wallet_status(self):
        response = requests.get(self.REST_ENDPOINT + '/wapi/v3/systemStatus.html')
        if response.status_code == 200:
            status = response.json()
            if status == 0:
                return True
        return False

    async def connect_to_ticker(self, url, on_message):
        uri = self.WS_ENDPOINT + url
        ws = await websockets.connect(uri)

        try:
            while True:
                msg = await ws.recv()
                on_message(msg, self.ID)
        except websockets.WebSocketException as wse:
            print(wse)
            pass
