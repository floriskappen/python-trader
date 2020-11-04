import yaml

from api.binance import Binance

secrets = None

with open('secrets.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    secrets = data

binance = Binance(secrets['keys']['binance']['key'], secrets['keys']['binance']['secret'])
