import helpers
from trader import Trader

def main():
    arguments = helpers.get_arguments()

    config = helpers.get_config(config_name=arguments['c'])
    secrets = helpers.get_secrets()
    helpers.validate_config(config)
    if 'period' in config:
        config['period'] = helpers.period_to_epoch(config['period'])
    trader = Trader(config, secrets)
    if config['type'] == 'backtest':
        trader.backtest(config['period'])

if __name__ == "__main__":
   main()
