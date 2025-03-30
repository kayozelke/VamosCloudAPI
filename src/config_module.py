import configparser
import os

DEFAULT_CONF = {
    'DATABASE' : {
        'username' : 'admin',
        'password' : 'admin',
        'host'     : 'localhost',
        'port'     : '3306',
        'database' : 'vamos_cloud_app'
    }
}

def writeConfigIfNotExists(config_path = 'config.ini'):
    if not os.path.exists(config_path):
        config = configparser.ConfigParser()
        config.read_dict(DEFAULT_CONF)
        with open(config_path, 'w') as configfile:
            config.write(configfile)
            configfile.close()
            return True
    else:
        return False
        


def loadConfig(config_path = 'config.ini', createIfNotExists = True):
    if createIfNotExists:
        writeConfigIfNotExists(config_path=config_path)
    config = configparser.ConfigParser()
    config.read(config_path)
    
    return {s:dict(config.items(s)) for s in config.sections()}