from api.binance import Binance
import helpers
import logging

def main():
    arguments = helpers.get_arguments()

    config = helpers.get_config(config_name=arguments['c'])
    secrets = helpers.get_secrets()
    helpers.validate_config(config)

    binance = Binance(secrets['keys']['binance']['key'], secrets['keys']['binance']['secret'])

if __name__ == "__main__":
   main()
