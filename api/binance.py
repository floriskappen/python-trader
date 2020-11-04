import requests
import asyncio
import websockets

class Binance():
    REST_ENDPOINT = 'https://api.binance.com'
    WS_ENDPOINT = 'wss://stream.binance.com:9443'

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret
        self.check_status()
        asyncio.run(self.create_tasks())

    def check_status(self):
        wallet_up = self.check_wallet_status()

    def check_wallet_status(self):
        response = requests.get(self.REST_ENDPOINT + '/wapi/v3/systemStatus.html')
        if response.status_code == 200:
            status = response.json()
            if status == 0:
                return True
        return False

    async def create_tasks(self):
        task1 = asyncio.create_task(self.websocket1())
        task2 = asyncio.create_task(self.websocket2())

        await task1
        await task2

        await print('test')

    async def websocket1(self):
        uri = self.WS_ENDPOINT + '/ws/ethbtc@miniTicker@1000ms'
        async with websockets.connect(uri) as websocket:
            while True:
                response = await websocket.recv()
                print(response)
    async def websocket2(self):
        uri = self.WS_ENDPOINT + '/ws/bnbusdt@miniTicker@1000ms'
        async with websockets.connect(uri) as websocket:
            while True:
                response = await websocket.recv()
                print(response)