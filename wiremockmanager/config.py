import ConfigParser

Config = None

if Config is None:
    Config = ConfigParser.ConfigParser()
    Config.read('config.ini')