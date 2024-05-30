import os
import json
from models.secret import SecretModel
from models.config import ConfigModel

_root_dir = os.path.dirname(os.path.abspath(__file__))


def get_secret() -> SecretModel:
    """
    Get the SecretModel from secrets.json
    """
    with open(_root_dir + '/secrets.json', 'r') as json_file:
        _json = json.loads(json_file.read())
        return SecretModel(**_json)
    

def get_config() -> ConfigModel:
    """
    Get the ConfigModel from secrets.json
    """
    with open(_root_dir + '/config.json', 'r') as json_file:
        _json = json.loads(json_file.read())
        return ConfigModel(**_json)