import argparse
import yaml
import os

def get_arguments():
    parser = argparse.ArgumentParser(description='Set a config file.')
    parser.add_argument('-c', help='Config file to be used')
    arguments = parser.parse_args()
    arguments_dictionary = vars(arguments)
    if not arguments_dictionary['c']:
        print('ERROR: Please enter -c for config file to be used')
        exit();
    return arguments_dictionary

def get_config(config_name):
    if not os.path.isfile('./config/{config}.yaml'.format(config=config_name)):
        print("ERROR: Entered config file name does not exist. Don't inclode .yaml when inputting the name.")
        exit()
    with open('./config/{config}.yaml'.format(config=config_name)) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print('SUCCESS: Loaded configiration {config}'.format(config=config_name))
        return data

def get_secrets():
    if not os.path.isfile('./secrets.yaml'):
        print('ERROR: Please make sure there is a secrets.yaml in the root directory.')
        exit()
    with open('./secrets.yaml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        print('SUCCESS: Loaded secrets')
        return data


import config.constants as config_constants
def validate_config(config):
    # Check config type
    if not config['type'] in config_constants.TYPE:
        print('ERROR: Configured type "{type}" is not supported'.format(type=config['type']))
        exit()

    # Check keys in config file
    for key in config_constants.GLOBAL_KEYS:
        if not key in config.keys():
            print('ERROR: Missing configured key "{key}"'.format(key=key))
            exit()

    # Check keys in config file depending on type
    for key in config_constants.TYPE_KEYS[config['type']]:
        if not key in config.keys():
            print('ERROR: Missing configured key "{key}"'.format(key=key))
            exit()

    # Check config exchange
    if not config['exchange'] in config_constants.EXCHANGE:
        print('ERROR: Configured exchange "{exchange}" is not supported'.format(exchange=config['exchange']))
        exit()

    # Check config strategy
    if not os.path.isfile('./strategy/{strategy}.py'.format(strategy=config['strategy'])):
        print('ERROR: Configured strategy "{strategy}" not found.'.format(strategy=config['strategy']))
        exit()
