import helpers
from trader import Trader

def main():
    arguments = helpers.get_arguments()

    config = helpers.get_config(config_name=arguments['c'])
    secrets = helpers.get_secrets()
    helpers.validate_config(config)
    trader = Trader(config, secrets)
    trader.start()

if __name__ == "__main__":
   main()
